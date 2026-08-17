from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('students.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return "Student Management System API"

@app.get("/about")
def about():
    return "A fully functional API to manage our student records"

@app.get("/all-students")
def all_student():
    data = load_data()
    return data