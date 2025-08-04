import re
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import date, datetime


# Модель Pydantic дял описания студента
class SStudent(BaseModel):
    # Тем самым Pydantic понимает явно, что работать он будет с аргументами базы данных.
    model_config = ConfigDict(from_attributes=True)
    id: int
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
    major_id: int = Field(default=..., ge=1,
                         description="ID специальности студента",)
    course: int = Field(default=..., ge=1, le=5,
                        description="Курс должен быть в диапазоне от 1 до 5",)
    special_notes: Optional[str] = Field(default=None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов",)
    # Дополнительное поле, используется для отображения названия факультета
    major: Optional[str] = Field(..., description="Название факультета")

    # Валидатор поля
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError("Номер телефона должен начинаться с + и содержать от 1 до 15 цифр")
        return values

    # Валидатор даты рождения
    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return values


# Модель Pydantic дял описания студента для его добавления
class SStudentAdd(BaseModel):
    # id будет сгенерировано базой данных
    phone_number: str = Field(default=...,
                              description="Номер телефона в международном формате, начинающийся с '+'", )
    first_name: str = Field(default=..., min_length=1, max_length=50,
                            description="Имя студента, от 1 до 50 символов", )
    last_name: str = Field(default=..., min_length=1, max_length=50,
                           description="Фамилия студента, от 1 до 50 символов", )
    date_of_birth: date = Field(default=...,
                                description="Дата рождения студента в формате ГГГГ-ММ-ДД", )
    email: EmailStr = Field(default=...,
                            description="Электронная почта студента", )
    address: str = Field(default=..., min_length=10, max_length=200,
                         description="Адрес студента, не более 200 символов", )
    enrollment_year: int = Field(default=..., ge=2002,
                                 description="Год поступления должен быть не меньше 2002", )
    major_id: int = Field(default=..., ge=1,
                          description="ID специальности студента", )
    course: int = Field(default=..., ge=1, le=5,
                        description="Курс должен быть в диапазоне от 1 до 5", )
    special_notes: Optional[str] = Field(default=None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов", )

    # Валидатор поля
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError("Номер телефона должен начинаться с + и содержать от 1 до 15 цифр")
        return values

    # Валидатор даты рождения
    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return values


# Модель Pydantic дял описания студента для его добавления
class SStudentUpdateCourse(BaseModel):
    id: int = Field(default=..., description="ID студента")
    course: int = Field(default=..., ge=1, le=5,
                        description="Курс должен быть в диапазоне от 1 до 5", )
