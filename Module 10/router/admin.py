from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users, Todos
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from router.auth import get_current_user

load_dotenv()

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/admin/todo')
def read_all_todos(user : user_dependency, db : db_dependency):

    user_role = user.get('role')

    if user is None or user_role != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized user")

    return db.query(Todos).all()