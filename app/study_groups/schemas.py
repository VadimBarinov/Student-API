from pydantic import BaseModel, Field


class SStudyGroupGet(BaseModel):
    id: int = Field(..., description="ID группы")
    name: str = Field(..., min_length=1, description="Название группы")


class SStudyGroupAdd(BaseModel):
    name: str = Field(..., min_length=1, description="Название группы")


class SStudyGroupUpdateName(BaseModel):
    id: int = Field(..., description="ID группы")
    name: str = Field(..., min_length=1, description="Новое название группы")
