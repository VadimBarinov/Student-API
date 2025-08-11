from pydantic import BaseModel, Field


# Модель Pydantic для добавления нового факультета
class SMajorsAdd(BaseModel):
    # id не указывается, так как база данных сама его генерирует
    major_name: str = Field(..., description="Название факультета")
    major_description: str = Field(None, description="Описание факультета")
    count_students: int = Field(0, description="Количество студентов")


# Модель Pydantic для обновления данных о факультете
class SMajorUpdateDescription(BaseModel):
    major_name: str = Field(..., description="Название факультета")
    major_description: str = Field(None, description="Новое описание факультета")


# Модель для получения факультета
class SMajorGet(BaseModel):
    id: int = Field(..., description="Id факультета")
    major_name: str = Field(..., description="Название факультета")
    major_description: str = Field(None, description="Описание факультета")
    count_students: int = Field(0, description="Количество студентов")