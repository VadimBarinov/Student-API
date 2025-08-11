from pydantic import BaseModel, Field


class SWeekdaysGet(BaseModel):
    id: int = Field(..., description="Id дня недели")
    name: str = Field(..., description="День недели")