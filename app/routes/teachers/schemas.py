import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


class STeacherGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    phone_number: str = Field(default=...,
                              description="Номер телефона в международном формате, начинающийся с '+'",)
    first_name: str = Field(default=..., min_length=1, max_length=50,
                            description="Имя преподавателя, от 1 до 50 символов",)
    last_name: str = Field(default=..., min_length=1, max_length=50,
                           description="Фамилия преподавателя, от 1 до 50 символов",)
    patronymic: str = Field(default=..., min_length=1, max_length=50,
                           description="Отчество преподавателя, от 1 до 50 символов",)
    date_of_birth: date = Field(default=...,
                                description="Дата рождения преподавателя в формате ГГГГ-ММ-ДД",)
    email: EmailStr = Field(default=...,
                            description="Электронная почта преподавателя",)
    address: str = Field(default=..., min_length=10, max_length=200,
                         description="Адрес преподавателя, не более 200 символов",)
    major_id: int = Field(default=..., ge=1,
                         description="ID специальности преподавателя",)
    special_notes: Optional[str] = Field(default=None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов",)
    major: Optional[str] = Field(..., description="Название факультета")

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


class STeacherAdd(BaseModel):
    phone_number: str = Field(default=...,
                              description="Номер телефона в международном формате, начинающийся с '+'",)
    first_name: str = Field(default=..., min_length=1, max_length=50,
                            description="Имя преподавателя, от 1 до 50 символов",)
    last_name: str = Field(default=..., min_length=1, max_length=50,
                           description="Фамилия преподавателя, от 1 до 50 символов",)
    patronymic: str = Field(default=..., min_length=1, max_length=50,
                           description="Отчество преподавателя, от 1 до 50 символов",)
    date_of_birth: date = Field(default=...,
                                description="Дата рождения преподавателя в формате ГГГГ-ММ-ДД",)
    email: EmailStr = Field(default=...,
                            description="Электронная почта преподавателя",)
    address: str = Field(default=..., min_length=10, max_length=200,
                         description="Адрес преподавателя, не более 200 символов",)
    major_id: int = Field(default=..., ge=1,
                         description="ID специальности преподавателя",)
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


class STeacherUpdatePhoneNumber(BaseModel):
    id: int = Field(..., description="ID преподавателя")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError("Номер телефона должен начинаться с + и содержать от 1 до 15 цифр")
        return values