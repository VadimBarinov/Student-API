from fastapi import APIRouter, HTTPException, status

from app.dependencies import SessionDep
from app.routes.teachers.dao import TeacherDAO
from app.routes.teachers.rb import RBTeacherDep
from app.routes.teachers.schemas import STeacherGet, STeacherAdd, STeacherUpdatePhoneNumber

router = APIRouter(
    prefix="/teachers",
    tags=["Работа с преподавателями", ],
)


@router.get("/", summary="Получить всех преподавателей по фильтру")
async def get_all_teachers(session: SessionDep, request_body: RBTeacherDep) -> list[STeacherGet] | dict:
    check_teacher = await TeacherDAO.find_teachers(session=session, **request_body.to_dict())
    if check_teacher is None or len(check_teacher) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Преподаватели не найдены!")
    return check_teacher


@router.get("/get_by_id/{teacher_id}/", summary="Получить одного преподавателя по ID")
async def get_teacher_by_id(session: SessionDep, teacher_id: int) -> STeacherGet | dict:
    check_teacher = await TeacherDAO.find_full_data(session=session, teacher_id=teacher_id)
    if check_teacher is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Преподаватель с ID {teacher_id} не найден!")
    return check_teacher


@router.post("/add/", summary="Добавить нового преподавателя")
async def add_teacher(session: SessionDep, teacher: STeacherAdd) -> dict:
    check_teacher = await TeacherDAO.add(session=session, **teacher.model_dump())
    if check_teacher:
        return {"message": "Преподаватель успешно добавлен!", "teacher": teacher}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при добавлении преподавателя")



@router.put("/update_phone_number/", summary="Обновить номер телефона преподавателя")
async def update_teacher_phone_number(session: SessionDep, teacher: STeacherUpdatePhoneNumber) -> dict:
    check_teacher = await TeacherDAO.update(
        session=session,
        filter_by={"id": teacher.id},
        phone_number=teacher.phone_number
    )
    if check_teacher:
        return {"message": "Номер телефона преподавателя успешно изменен!", "teacher": teacher}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при изменении номера телефона преподавателя")


@router.delete("/delete_by_id/{teacher_id}/", summary="Удалить преподавателя по ID")
async def delete_teacher(session: SessionDep, teacher_id: int) -> dict:
    check_teacher = await TeacherDAO.delete(session=session, id=teacher_id)
    if check_teacher:
        return {"message": f"Преподаватель с ID {teacher_id} успешно удален"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Ошибка при удалении преподавателя")