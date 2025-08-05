from pydantic import BaseModel, Field


class SSubjectGet(BaseModel):
    id: int = Field(..., description="ID предмета")
    name: str = Field(..., description="Название предмета")


class SSubjectAdd(BaseModel):
    name: str = Field(..., description="Название предмета")


class SSubjectUpdateName(BaseModel):
    id: int = Field(..., description="ID предмета")
    name: str = Field(..., description="Новое название предмета")
