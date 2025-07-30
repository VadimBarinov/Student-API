from fastapi import FastAPI
from utils import json_to_dict_list
import os
from typing import Optional


# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))
# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)
# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, "students.json")


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Hello, World!"}


# Optional позволяет не передавать этот параметр
@app.get("/students/{course}")
def get_all_students(
        course: int,
        major: Optional[str] = None,
        enrollment_year: Optional[int] = 2018
):
    students = json_to_dict_list(path_to_json)
    filtered_students = []

    for student in students:
        if student["course"] == course:
            filtered_students.append(student)
    if major:
        filtered_students = [
            student for student in filtered_students if student["major"].lower() == major.lower()
        ]
    if enrollment_year:
        filtered_students = [
            student for student in filtered_students if student["enrollment_year"] == enrollment_year
        ]
    return filtered_students


@app.get("/student/{student_id}")
def get_student_from_id(student_id: int):
    students = json_to_dict_list(path_to_json)
    for student in students:
        if student["student_id"] == student_id:
            return student
    return None


@app.get("/student")
def get_student_from_param_id(student_id: int):
    return get_student_from_id(student_id)