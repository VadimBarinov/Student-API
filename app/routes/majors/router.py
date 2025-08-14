from fastapi import APIRouter, HTTPException, status

from app.dependencies import SessionDep
from app.routes.majors.dao import MajorsDAO
from app.routes.majors.rb import RBMajorDep
from app.routes.majors.schemas import SMajorsAdd, SMajorUpdateDescription, SMajorGet

router = APIRouter(
    prefix="/majors", tags=["Работа с факультетами",]
)


@router.get("/", summary="Получить все факультеты по фильтру")
async def get_all_majors(session: SessionDep, request_body: RBMajorDep) -> list[SMajorGet] | dict:
    check_major = await MajorsDAO.find_all(session=session, **request_body.to_dict())
    if check_major is None or len(check_major) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Факультеты не найдены!")
    return check_major


@router.get("/get_by_id/{major_id}/", summary="Получить один факультет по ID")
async def get_major_by_id(session: SessionDep, major_id: int) -> SMajorGet | dict:
    check_major = await MajorsDAO.find_one_or_none_by_id(session=session, data_id=major_id)
    if check_major is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Факультет с ID {major_id} не найден!")
    return check_major


@router.get("/get_by_filter/", summary="Получить один факультет по фильтру")
async def get_major_by_filter(session: SessionDep, request_body: RBMajorDep) -> SMajorGet | dict:
    check_major = await MajorsDAO.find_one_or_none(session=session, **request_body.to_dict())
    if check_major is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Факультет с указанными вами параметрами не найден!")
    return check_major


@router.post("/add/", summary="Добавить новый факультет")
async def add_major(session: SessionDep, major: SMajorsAdd) -> dict:
    check_major = await MajorsDAO.add(session=session, **major.model_dump())
    if check_major:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при добавлении факультета!")


@router.put("/update_description/", summary="Обновить описания факультета")
async def update_major_description(session: SessionDep, major: SMajorUpdateDescription) -> dict:
    check_major = await MajorsDAO.update(
        session=session,
        filter_by={"major_name": major.major_name,},
        major_description=major.major_description
    )
    if check_major:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при обновлении описания факультета!")


@router.delete("/delete_by_id/{major_id}/", summary="Удалить факультет по ID")
async def delete_major(session: SessionDep, major_id: int) -> dict:
    check_major = await MajorsDAO.delete(session=session, id=major_id)
    if check_major:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Ошибка при удалении факультета!")
