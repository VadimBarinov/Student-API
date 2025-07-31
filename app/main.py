from fastapi import FastAPI, Depends, HTTPException

from utils import json_to_dict_list, add_student, upd_student, dell_student

from typing import Optional, List, Any

from enum import Enum
from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError
from datetime import datetime, date
import re


class Major(str, Enum):
        informatics = "Информатика"
        economics = "Экономика"
        law = "Право"
        medicine = "Медицина"
        engineering = "Инженерия"
        psychology = "Психология"
        languages = "Языки"
        ecology = "Экология"
        mathematics = "Математика"


class SStudent(BaseModel):
    student_id: int
    phone_number: str = Field(default=...,
                              description="Номер телефона в международном формате, начинающийся с '+'",)
    first_name: str = Field(default=..., min_length=1, max_length=50,
                            description="Имя студента, от 1 до 50 символов",)
    last_name: str = Field(default=..., min_length=1, max_length=50,
                           description="Фамилия студента, от 1 до 50 символов",)
    date_of_birth: date = Field(default=...,
                                description="Дата рождения студента в формате ГГГГ-ММ-ДД",)
    email: EmailStr = Field(default=...,
                            description="Электронная почта студента",)
    address: str = Field(default=..., min_length=10, max_length=200,
                         description="Адрес студента, не более 200 символов",)
    enrollment_year: int = Field(default=..., ge=2002,
                                 description="Год поступления должен быть не меньше 2002",)
    major: Major = Field(default=...,
                         description="Специальность студента",)
    course: int = Field(default=..., ge=1, le=5,
                        description="Курс должен быть в диапазоне от 1 до 5",)
    special_notes: Optional[str] = Field(default=None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов",)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError("Номер телефона должен начинаться с + и содержать от 1 до 15 цифр")
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return values


# Request Body Student
class RBStudent:
    # Optional позволяет не передавать этот параметр
    def __init__(self, course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
        self.course = course
        self.major = major
        self.enrollment_year = enrollment_year


class SUpdateFilter(BaseModel):
    student_id: int


class SStudentUpdate(BaseModel):
    course: int = Field(..., ge=1, le=5,
                        description="Курс должен быть в диапазоне от 1 до 5")
    major: Optional[Major] = Field(...,
                                   description="Специальность студента")


class SDeleteFilter(BaseModel):
    key: str
    value: Any


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Hello, World!"}


@app.get("/students/{course}")
def get_all_students(request_body: RBStudent = Depends()) -> List[SStudent]:
    students = json_to_dict_list()
    filtered_students = []

    for student in students:
        if student["course"] == request_body.course:
            filtered_students.append(student)
    if request_body.major:
        filtered_students = [
            student for student in filtered_students if student["major"].lower() == request_body.major.lower()
        ]
    if request_body.enrollment_year:
        filtered_students = [
            student for student in filtered_students if student["enrollment_year"] == request_body.enrollment_year
        ]
    return filtered_students


@app.get("/student/{student_id}")
def get_student_from_id(student_id: int) -> SStudent | None:
    students = json_to_dict_list()
    for student in students:
        if student["student_id"] == student_id:
            return student
    return None


@app.get("/student")
def get_student_from_param_id(student_id: int) -> SStudent | None:
    return get_student_from_id(student_id)


@app.post("/add_student")
def add_student_handler(student: SStudent):
    student_dict = student.model_dump()
    check_student = add_student(student_dict)
    if check_student:
        return {"message": "Студент успешно добавлен!"}
    else:
        return  {"message": "Ошибка при добавлении студента!"}


@app.put("/update_student")
def update_student_handler(filter_student: SUpdateFilter, new_data: SStudentUpdate):
    check_student = upd_student(filter_student.model_dump(), new_data.model_dump())
    if check_student:
        return {"message": "Информация о студенте успешно обновлена!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о студенте")


@app.delete("/delete_student")
def delete_student_handler(filter_student: SDeleteFilter):
    check_student = dell_student(filter_student.key, filter_student.value)
    if check_student:
        return {"message": "Студент успешно удален!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении студента")