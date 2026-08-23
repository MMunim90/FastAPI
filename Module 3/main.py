from fastapi import FastAPI, Path, HTTPException, Query
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
def single_student(student_id: str = Path(..., description="Student id of the student", example="S001")):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail='Student not found!!!')
    
    
    
@app.get("/sort")
def sort_student(sorted_by: str = Query(..., description="Sort on the basis of class, age, roll, marks"), ):
    
    valid_fields = ["age", "class", "roll", "math_marks", "english_marks", "science_marks"]
    
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid field, select from {valid_fields}')
    
    data = load_data()
    
    sorted_data = list(data.values())
    sorted_data.sort(key = lambda x:x[sorted_by], reverse=True)
    
    return sorted_data