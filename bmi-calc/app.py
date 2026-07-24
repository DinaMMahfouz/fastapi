from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

students={
    1:{
        "name": "Dina", "age":"28","classes":"Maths"
    }
}

class Student(BaseModel):
    name: str
    age: int
    classes: str
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    classes: Optional[str] = None
    

@app.get("/")
def home():
    return {"message": "FastAPI is working"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    id = int(student_id)
    return students[id]


@app.get("/get-by-name")
def get_by_name(name: str):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"message": "No student found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"message": "Student already exists"}
    
    students[student_id] = student
    return students[student_id]
    
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"message": "Student does not exist"}
    
    if student.name != None:
        students[student_id].name = student.name
        
    if student.age != None:
        students[student_id].age = student.age
    
    if student.classes != None:
        students[student_id].id = student.classes
        
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"message": "Student does not exist"}
    
    del students[student_id]
    return {"message": "Student deleted"}