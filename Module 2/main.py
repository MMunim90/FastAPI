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


@app.get("/all-students/{student_id}")
def single_student(student_id: str):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        return "Student not found!!!"