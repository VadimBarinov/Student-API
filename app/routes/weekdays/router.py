from fastapi import APIRouter, HTTPException, status

from app.routes.weekdays.dao import WeekdayDAO
from app.routes.weekdays.schemas import SWeekdaysGet


router = APIRouter(
    prefix="/weekdays",
    tags=["Дни недели", ]
)


@router.get("/", summary="Получить все дни недели")
async def get_all_weekdays() -> list[SWeekdaysGet]:
    check_weekdays = await WeekdayDAO.find_all()
    if check_weekdays is None or len(check_weekdays) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Информация не найдена")
    return check_weekdays