from pydantic import BaseModel, Field


class SStudyGroupGet(BaseModel):
    id: int = Field(..., description="ID группы")
    name: str = Field(..., min_length=1, description="Название группы")
    count_students: int = Field(0, description="Количество студентов")


class SStudyGroupAdd(BaseModel):
    name: str = Field(..., min_length=1, description="Название группы")
    count_students: int = Field(0, description="Количество студентов")


class SStudyGroupUpdateName(BaseModel):
    id: int = Field(..., description="ID группы")
    name: str = Field(..., min_length=1, description="Новое название группы")
