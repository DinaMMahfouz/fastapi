from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
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


# Always create/open the database beside this Python file
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "school_database.db"


class Student(BaseModel):
    name: str
    age: int
    grade: int


def setup_db():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade INTEGER NOT NULL
            )
        """)

        conn.commit()


setup_db()


@app.get("/")
async def read_students():
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            students = cursor.execute(
                "SELECT * FROM students"
            ).fetchall()

            return [dict(student) for student in students]

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )


@app.post("/students/")
async def create_student(new_student: Student):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO students (name, age, grade)
                VALUES (?, ?, ?)
                """,
                (
                    new_student.name,
                    new_student.age,
                    new_student.grade
                )
            )

            conn.commit()

            return {
                "message": "Student added successfully",
                "student_id": cursor.lastrowid
            }
            

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )
        
@app.put("/students/{student_id}")
async def update_student(student_id: int, update_student: Student):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE students
                SET name = ?, age = ?, grade = ?
                WHERE id = ?
                """,
                (
                    update_student.name,
                    update_student.age,
                    update_student.grade,
                    student_id
                )
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"Student with id {student_id} not found"
                )

            conn.commit()

            return {
                "message": "Student updated successfully"
            }

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )


@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM students
                WHERE id = ?
                """,
                (
                    student_id
                )
            )

            conn.commit()

            return {
                "message": "Student deleted successfully"
            }

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )
