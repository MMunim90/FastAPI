from fastapi import FastAPI, Path, HTTPException, Query, Body
import json

app = FastAPI()

def load_data():
    with open('books.json', 'r') as f:
        data = json.load(f)
    return data

def upload_data(data):
    with open('books.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return "Books Management System API"

@app.get("/about")
def about():
    return "A fully functional API to manage Books records"

@app.get("/books")
def all_books():
    data = load_data()
    return data


@app.get("/books/{book_id}")
def single_book(book_id: int = Path(..., description="book id of the book", example=1)):
    data = load_data()

    for book in data:
        if book["book_id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail='Book not found!!!')
    
    
    
@app.get("/sort")
def sort_books(sorted_by: str = Query(..., description="Sort books on the basis of pages, rating"), order: str = Query('desc', description="choose order: asc or desc")):
    
    valid_fields = ["pages", "rating"]
    
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Choose between asc or desc")
    
    data = load_data()
    
    
    if order == 'asc':
        data.sort(key = lambda x:x[sorted_by])
        return data
    
    else:
        data.sort(key = lambda x:x[sorted_by], reverse=True)
        return data
    
    
    
# post request
@app.post("/create_books")
def add_book(book: dict = Body()):
    data = load_data()
    data.append(book)
    upload_data(data)
    return "New books added successfully!!!"