from fastapi import APIRouter

from app.majors.dao import MajorsDAO
from app.majors.schemas import SMajorsAdd


router = APIRouter(
    prefix="/majors", tags=["Работа с факультетами",]
)


@router.post("/add/", summary="Добавление нового факультета")
async def add_major(major: SMajorsAdd) -> dict:
    check_major = await MajorsDAO.add(**major.model_dump())
    if check_major:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        return {"message": "Ошибка при добавлении факультета!"}