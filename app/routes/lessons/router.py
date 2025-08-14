from fastapi import APIRouter, Depends, HTTPException, status

from app.routes.lessons.dao import LessonDAO
from app.routes.lessons.rb import RBLesson
from app.routes.lessons.schemas import SLessonGet, SLessonAdd, SLessonUpdateAuditorium

router = APIRouter(
    prefix="/lessons",
    tags=["Работа с занятиями",],
)


@router.get("/", summary="Получить все занятия по фильтру")
async def get_all_lessons_by_filter(lesson: RBLesson = Depends()) -> list[SLessonGet] | dict:
    check_lesson = await LessonDAO.find_lessons(**lesson.to_dict())
    if check_lesson is None or len(check_lesson) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Занятия не найдены!")
    return check_lesson


@router.get("/get_by_id/{lesson_id}/", summary="Получить занятие по ID")
async def get_lesson_by_id(lesson_id: int) -> SLessonGet | dict:
    check_lesson = await LessonDAO.find_all_data(lesson_id=lesson_id)
    if check_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Занятие с ID {lesson_id} не найдено!")
    return check_lesson


@router.post("/add/", summary="Добавить новое занятие")
async def add_new_lesson(lesson: SLessonAdd) -> dict:
    check_lesson = await LessonDAO.add(**lesson.model_dump())
    if check_lesson:
        return {"message": "Занятие успешно добавлено!", "lesson": lesson}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при добавлении занятия!")


@router.put("/update_auditorium/", summary="Изменить аудиторию")
async def update_lesson_auditorium(lesson: SLessonUpdateAuditorium) -> dict:
    check_lesson = await LessonDAO.update(
        filter_by={"id": lesson.id, },
        auditorium=lesson.auditorium
    )
    if check_lesson:
        return {"message": "Аудитория успешно изменена!", "lesson": lesson}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при изменении аудитории!")


@router.delete("/delete_by_id/{lesson_id}/", summary="Удалить занятие по ID")
async def delete_lesson_by_id(lesson_id: int) -> dict:
    check_lesson = await LessonDAO.delete(id=lesson_id)
    if check_lesson:
        return {"message": f"Занятие с ID {lesson_id} успешно удалено!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Ошибка при удалении занятия!")
