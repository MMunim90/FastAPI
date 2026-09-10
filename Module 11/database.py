from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db' # this is for sqlite database

SQLALCHEMY_DATABASE_URL='postgresql://postgres:password@localhost/ToDoApplicationDatabase' # this is for postgresql database

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()