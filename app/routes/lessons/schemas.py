import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SLessonGet(BaseModel):
    id: int = Field(..., description="ID занятия")
    study_group_id: int = Field(..., description="ID учебной группы")
    subject_id: int = Field(..., description="ID предмета")
    teacher_id: int = Field(..., description="ID преподавателя")
    weekday_id: int = Field(..., description="ID дня недели")
    lesson_number: int = Field(...,ge=1, le=10,
                               description="Номер занятия от 1 до 10")
    auditorium: str = Field(...,
                            description="Название аудитории в формате 'номер_корпуса/номер_аудитории'")

    study_group: Optional[str] = Field(..., description="Название учебной группы")
    subject: Optional[str] = Field(..., description="Название предмета")
    teacher: Optional[str] = Field(..., description="Имя преподавателя")
    weekday: Optional[str] = Field(..., description="День недели")

    @field_validator("auditorium")
    @classmethod
    def auditorium_validator(cls, values: str) -> str:
        if not re.match(r"^\d{1,10}/\d{1,10}$", values):
            raise ValueError("Название аудитории должно быть в формате 'номер_корпуса/номер_аудитории'")
        return values


class SLessonAdd(BaseModel):
    study_group_id: int = Field(..., description="ID учебной группы")
    subject_id: int = Field(..., description="ID предмета")
    teacher_id: int = Field(..., description="ID преподавателя")
    weekday_id: int = Field(..., description="ID дня недели")
    lesson_number: int = Field(...,ge=1, le=10,
                               description="Номер занятия от 1 до 10")
    auditorium: str = Field(...,
                            description="Название аудитории в формате 'номер_корпуса/номер_аудитории'")

    @field_validator("auditorium")
    @classmethod
    def auditorium_validator(cls, values: str) -> str:
        if not re.match(r"^\d{1,10}/\d{1,10}$", values):
            raise ValueError("Название аудитории должно быть в формате 'номер_корпуса/номер_аудитории'")
        return values


class SLessonUpdateAuditorium(BaseModel):
    id: int = Field(..., description="ID занятия")
    auditorium: str = Field(...,
                            description="Название новой аудитории в формате 'номер_корпуса/номер_аудитории'")

    @field_validator("auditorium")
    @classmethod
    def auditorium_validator(cls, values: str) -> str:
        if not re.match(r"^\d{1,10}/\d{1,10}$", values):
            raise ValueError("Название аудитории должно быть в формате 'номер_корпуса/номер_аудитории'")
        return values