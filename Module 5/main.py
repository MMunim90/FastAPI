from fastapi import FastAPI, Path, HTTPException, Query, Body
import json

app = FastAPI()

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
def single_student(student_id: str = Path(..., description="Student id of the student", example="S001")):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail='Student not found!!!')
    
    
    
@app.get("/sort")
def sort_student(sorted_by: str = Query(..., description="Sort on the basis of class, age, roll, marks"), order: str = Query('asc', description="choose order: asc or desc")):
    
    valid_fields = ["age", "class", "roll", "math_marks", "english_marks", "science_marks"]
    
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
def add_new_student(student: dict = Body()):
    data = load_data()
    
    student_id = student["id"]
    data[student_id] = student
    del data[student_id]["id"]
    
    upload_data(data)
    return "Successfully student created!!!"