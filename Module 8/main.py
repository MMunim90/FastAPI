from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from models import Movies
from database import engine, SessionLocal
from fastapi.responses import JSONResponse

app = FastAPI()

class MovieCreate(BaseModel):
    movie_id : int 
    title : str
    director : str = Field(max_length=100)
    genre : str
    duration : int = Field(ge=0)
    rating : float = Field(ge=0, lt=6)

class MovieUpdate(BaseModel):
    title : Optional[str] = Field(default=None)
    director : Optional[str] = Field(default=None, max_length=100)
    genre : Optional[str] = Field(default=None)
    duration : Optional[int] = Field(default=None, ge=0)
    rating : Optional[float] = Field(default=None, ge=0, lt=6)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/movies')
def get_all_movies(db : db_dependency):
    return db.query(Movies).all()


@app.get("/movies/sort")
def sort_movies(db : db_dependency, sort_by: str = Query('rating', description="Sort movies on the basis of duration, rating"), order: str = Query('desc', description="choose order: asc or desc")):
    
    valid_fields = ["duration", "rating"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Choose between asc or desc")
    
    data = db.query(Movies).all()  
    
    if order == 'asc':
        data.sort(key = lambda movie:getattr(movie, sort_by))
        return data
    
    else:
        data.sort(key = lambda movie:getattr(movie, sort_by), reverse=True)
        return data


@app.get('/movies/{movie_id}')
def get_specific_movies(db : db_dependency, movie_id : int):
    specific_movie = db.query(Movies).filter(Movies.movie_id == movie_id).first()

    if specific_movie is not None:
        return specific_movie
    else:
        raise HTTPException(status_code=404, detail='Movie Not Found')


@app.post('/create_movies')
def create_movies(db : db_dependency, new_movie : MovieCreate):

    if new_movie.duration < 0:
        raise HTTPException(status_code=422, detail='Movie duration cannot be negetive!!!')

    specific_movie = db.query(Movies).filter(Movies.movie_id == new_movie.movie_id).first()
    
    if specific_movie is not None:
        raise HTTPException(status_code=400, detail='Movie is already exists!!!')

    valid_genre = ["action", "comedy", "drama", "thriller"]

    if new_movie.genre not in valid_genre:
        raise HTTPException(status_code=422, detail=f'Invalid genre, select from {valid_genre}')

    movie_model = Movies(**new_movie.model_dump())
    db.add(movie_model)
    db.commit()

    return JSONResponse(status_code=201, content={'message' : 'Movie created successfully'})



@app.put('/movies/{movie_id}')
def update_movies(db : db_dependency, movie_id : int, update_movie : MovieUpdate):
    movie = db.query(Movies).filter(Movies.movie_id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail='Movie Not Found')

    update_data = update_movie.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(movie,key,value)

    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Movie updated successfully'})


@app.delete('/movies/{movie_id}')
def delete_movies(db : db_dependency, movie_id : int):

    movie = db.query(Movies).filter(Movies.movie_id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail='Movie Not Found')

    db.query(Movies).filter(Movies.movie_id == movie_id).delete()

    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Movie deleted successfully'})