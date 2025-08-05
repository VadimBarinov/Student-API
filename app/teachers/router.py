from fastapi import APIRouter, Depends

from app.teachers.dao import TeacherDAO
from app.teachers.rb import RBTeacher
from app.teachers.schemas import STeacherGet

router = APIRouter(
    prefix="/teachers",
    tags=["Работа с преподавателями", ],
)


@router.get("/", summary="Получить всех преподавателей по фильтру")
async def get_all_teachers(request_body: RBTeacher = Depends()) -> list[STeacherGet] | dict:
    check_teacher = await TeacherDAO.find_teachers(**request_body.to_dict())
    if check_teacher is None or len(check_teacher) == 0:
        return {"message": f"Преподаватели не найдены!"}
    return check_teacher


@router.get("/get_by_id/{teacher_id}/", summary="Получить одного преподавателя по ID")
async def get_teacher_by_id(teacher_id: int) -> STeacherGet | dict:
    check_teacher = await TeacherDAO.find_full_data(teacher_id)
    if check_teacher is None:
        return {"message": f"Преподаватель с ID {teacher_id} не найден!"}
    return check_teacher

# Нужно дописать запросы:
# POST
# PUT
# DELETE