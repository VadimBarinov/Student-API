from fastapi import APIRouter

from app.weekdays.dao import WeekdayDAO
from app.weekdays.schemas import SWeekdaysGet


router = APIRouter(
    prefix="/weekdays",
    tags=["Дни недели", ]
)


@router.get("/", summary="Получить все дни недели")
async def get_all_weekdays() -> list[SWeekdaysGet] | dict:
    check_weekdays = await WeekdayDAO.find_all()
    if check_weekdays is None or len(check_weekdays) == 0:
        return {"message": "Ошибка с получением информации"}
    return check_weekdays