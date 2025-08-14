import re
from pydantic import BaseModel, Field, EmailStr, field_validator


class SUserRegister(BaseModel):
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., description="Имя, от 2 до 50 символов")
    last_name: str = Field(..., description="Фамилия, от 2 до 50 символов")
    patronymic: str = Field(..., description="Отчество, от 2 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

    @field_validator("phone_number")
    @classmethod
    def validator_phone_number(cls, values: str) -> str:
        if not re.match(r"^\+\d{5,15}$", values):
            raise ValueError("Номер телефона должен начинаться с '+' и содержать от 5 до 15 цифр")
        return values


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserGet(BaseModel):
    id: int = Field(..., description="ID пользователя")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., description="Имя, от 2 до 50 символов")
    last_name: str = Field(..., description="Фамилия, от 2 до 50 символов")
    patronymic: str = Field(..., description="Отчество, от 2 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, description="Хэш пароля")

    is_user: bool = Field(..., description="Пользователь")
    is_student: bool = Field(..., description="Студент")
    is_teacher: bool = Field(..., description="Преподаватель")
    is_admin: bool = Field(..., description="Админ")
    is_super_admin: bool = Field(..., description="Супер админ")

    @field_validator("phone_number")
    @classmethod
    def validator_phone_number(cls, values: str) -> str:
        if not re.match(r"^\+\d{5,15}$", values):
            raise ValueError("Номер телефона должен начинаться с '+' и содержать от 5 до 15 цифр")
        return values


class SAddOrDeleteRoleToUser(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    role_name: str = Field(
        ...,
        examples=["is_user", "is_student", "is_teacher", "is_admin", "is_super_admin",],
        description="Роль, которую нужно добавить пользователю",
    )
