from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    id: int
    name: str
    grade: int

students = [
    {
        "id": 1,
        "name": "John Doe",
        "grade": 10
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "grade": 9
    },
    {
        "id": 3,
        "name": "Alice Brown",
        "grade": 8
    }
]

@app.get("/")
def read_students():
    return students

@app.post("/students/")
def create_student(New_Student: Student):
    students.append(New_Student)
    return students

@app.put("/students/{student_id}")
def read_student(student_id: int, update_student: Student):
    for index,student in students:
        if student["id"] == student_id:
            students[index] == update_student
            return update_student
    return {"message": "Student not found"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index,student in enumerate(students):
        if student["id"] == student_id:
            del students[index]
            return {"message": "Student deleted"}
    return {"message": "Student not found"}