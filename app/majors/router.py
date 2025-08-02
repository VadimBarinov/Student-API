from fastapi import APIRouter

from app.majors.dao import MajorsDAO
from app.majors.schemas import SMajorsAdd, SMajorUpdateDescription

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


@router.put("/update_description/", summary="Обновление описания факультета")
async def update_major_description(major: SMajorUpdateDescription) -> dict:
    check_major = await MajorsDAO.update(
        filter_by={"major_name": major.major_name,},
                   major_description=major.major_description
    )
    if check_major:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        return {"message": "Ошибка при обновлении описания факультета!"}


@router.delete("/delete/{major_id}/", summary="Удаление факультета")
async def delete_major(major_id: int) -> dict:
    check_major = await MajorsDAO.delete(id=major_id)
    if check_major:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        return {"message": "Ошибка при удалении факультета!"}


# ----------------------------------------------------------------------------------
# Нужно добавить эндпоинты:
# GET на получение записи по ID
# GET на получение записи по фильтру
# GET на получение всех записей
# ----------------------------------------------------------------------------------