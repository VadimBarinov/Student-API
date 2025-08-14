from fastapi import APIRouter, Depends, HTTPException, status
from app.routes.majors.dao import MajorsDAO
from app.routes.majors.rb import RBMajor
from app.routes.majors.schemas import SMajorsAdd, SMajorUpdateDescription, SMajorGet

router = APIRouter(
    prefix="/majors", tags=["Работа с факультетами",]
)


@router.get("/", summary="Получить все факультеты по фильтру")
async def get_all_majors(request_body: RBMajor = Depends()) -> list[SMajorGet] | dict:
    check_major = await MajorsDAO.find_all(**request_body.to_dict())
    if check_major is None or len(check_major) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Факультеты не найдены!")
    return check_major


@router.get("/get_by_id/{major_id}/", summary="Получить один факультет по ID")
async def get_major_by_id(major_id: int) -> SMajorGet | dict:
    check_major = await MajorsDAO.find_one_or_none_by_id(data_id=major_id)
    if check_major is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Факультет с ID {major_id} не найден!")
    return check_major


@router.get("/get_by_filter/", summary="Получить один факультет по фильтру")
async def get_major_by_filter(request_body: RBMajor = Depends()) -> SMajorGet | dict:
    check_major = await MajorsDAO.find_one_or_none(**request_body.to_dict())
    if check_major is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Факультет с указанными вами параметрами не найден!")
    return check_major


@router.post("/add/", summary="Добавить новый факультет")
async def add_major(major: SMajorsAdd) -> dict:
    check_major = await MajorsDAO.add(**major.model_dump())
    if check_major:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при добавлении факультета!")


@router.put("/update_description/", summary="Обновить описания факультета")
async def update_major_description(major: SMajorUpdateDescription) -> dict:
    check_major = await MajorsDAO.update(
        filter_by={"major_name": major.major_name,},
        major_description=major.major_description
    )
    if check_major:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при обновлении описания факультета!")


@router.delete("/delete_by_id/{major_id}/", summary="Удалить факультет по ID")
async def delete_major(major_id: int) -> dict:
    check_major = await MajorsDAO.delete(id=major_id)
    if check_major:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Ошибка при удалении факультета!")
