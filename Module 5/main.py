from fastapi import FastAPI, Path, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import Annotated, Optional
import json
from fastapi.responses import JSONResponse

app = FastAPI()

class Student(BaseModel):
    id: Annotated[str, Field(..., description="Student id of the student", json_schema_extra={"example": "S001"})]
    name: Annotated[str, Field(..., description="Name of the student", json_schema_extra={"example": "Karim Benzema"})]
    age: Annotated[int, Field(..., gt=2, lt=36, description="Age of the student", json_schema_extra={"example": 12})]
    student_class: Annotated[int, Field(..., gt=0, lt=13, description="Class of the student", json_schema_extra={"example": 7})]
    roll: Annotated[int, Field(..., gt=0, description="Roll of the student", json_schema_extra={"example": 1})]
    math_marks: Annotated[int, Field(..., gt=0, lt=101, description="Math Marks of the student", json_schema_extra={"example": 94})]
    english_marks: Annotated[int, Field(..., gt=0, lt=101, description="English Marks of the student", json_schema_extra={"example": 85})]
    science_marks: Annotated[int, Field(..., gt=0, lt=101, description="Science Marks of the student", json_schema_extra={"example": 97})]
    phone: Annotated[str, Field(..., description="Phone Number of the student", json_schema_extra={"example": "01XXX-XXXXXX"})]



class StudentUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    student_class: Annotated[Optional[int], Field(default=None)]
    roll: Annotated[Optional[int], Field(default=None)]
    math_marks: Annotated[Optional[int], Field(default=None)]
    english_marks: Annotated[Optional[int], Field(default=None)]
    science_marks: Annotated[Optional[int], Field(default=None)]
    phone: Annotated[Optional[str], Field(default=None)]



def load_data():
    with open('students.json', 'r') as f:
        data = json.load(f)
    return data

def upload_data(data):
    with open('students.json', 'w') as f:
        json.dump(data, f)

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
def single_student(student_id: str = Path(..., description="Student id of the student", examples="S001")):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail='Student not found!!!')
    
    
    
@app.get("/sort")
def sort_student(sorted_by: str = Query(..., description="Sort on the basis of student_class, age, roll, marks"), order: str = Query('asc', description="choose order: asc or desc")):
    
    valid_fields = ["age", "student_class", "roll", "math_marks", "english_marks", "science_marks"]
    
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Choose between asc or desc")
    
    data = load_data()
    
    
    # 1
    # sort_order = True if order == 'desc' else False
    
    # sorted_data = list(data.values())
    # sorted_data.sort(key = lambda x:x[sorted_by], reverse=sort_order)
    
    
    # 2
    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key = lambda x:x[sorted_by])
        return sorted_data
    
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key = lambda x:x[sorted_by], reverse=True)
        return sorted_data
    
    
    
# post request
@app.post("/add_new_student")
def add_new_student(student: Student):
    data = load_data()

    if student.id in data:
        raise HTTPException(status_code=400, detail='Student id already exists!!!')

    # 1
    # student_id = student.id
    # data[student_id] = student.model_dump()
    # del data[student_id]["id"]

    # 2
    data[student.id] = student.model_dump(exclude=["id"])
    
    upload_data(data)
    return JSONResponse(status_code= 201, content={'message': 'Successfully student created!!!'})



# put request
@app.put("/update_student/{student_id}")
def update_student(student_id: str, student: Student):
    data = load_data()

    if student.id in data:
        raise HTTPException(status_code=400, detail='Student id already exists!!!')

    # 1
    # student_id = student.id
    # data[student_id] = student.model_dump()
    # del data[student_id]["id"]

    # 2
    data[student.id] = student.model_dump(exclude=["id"])
    
    upload_data(data)
    return JSONResponse(status_code= 201, content={'message': 'Successfully student created!!!'})