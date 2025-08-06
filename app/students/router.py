from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent, SStudentAdd, SStudentUpdateCourse

# Создание роутера
# prefix устанавливает префикс для всех маршрутов роутера
# tags добавляет тег роутеру, будет использоваться в документации
router = APIRouter(
    prefix="/students", tags=["Работа со студентами", ]
)


# эндпоинт роутер для получения всех студентов
# summary это описание, будет показываться в документации
@router.get("/", summary="Получить всех студентов по фильтру")
# Начало асинхронной функции
# Асинхронность позволяет обрабатывать несколько запросов одновременно, не блокируя другие операции
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent] | dict:
    check_student = await StudentDAO.find_students(**request_body.to_dict())
    if check_student is None or len(check_student) == 0:
        return {"message": f"Студенты не найдены!"}
    return check_student


# получение студента по id
@router.get("/get_by_id/{student_id}/", summary="Получить одного студента по ID")
async def get_student_by_id(student_id: int) -> SStudent | dict:
    check_student = await StudentDAO.find_full_data(student_id)
    # Обработчик None
    if check_student is None:
        return {"message": f"Студент с ID {student_id} не найден!"}
    return check_student


# Получение студента с учетом переданного фильтра
# Используется Request Body Student из rb.py
@router.get("/get_by_filter/", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudent | dict:
    check_student = await StudentDAO.find_one_or_none(**request_body.to_dict())
    # Обработчик None
    if check_student is None:
        return {"message": f"Студент с указанными вами параметрами не найден!"}
    return check_student


@router.post("/add/", summary="Добавить нового студента")
async def add_student(student: SStudentAdd) -> dict:
    check_student = await StudentDAO.add(**student.model_dump())
    if check_student:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}


@router.put("/update_course/", summary="Обновить курс студента")
async def update_student_course(student: SStudentUpdateCourse) -> dict:
    check_student = await StudentDAO.update(
        filter_by={"id":student.id,},
        course=student.course
    )
    if check_student:
        return {"message": "Информация о курсе успешно обновлена!", "student": student}
    else:
        return {"message": "Ошибка при обновлении информации о курсе студента"}


@router.delete("/delete_by_id/{student_id}/", summary="Удалить студента по ID")
async def delete_student_by_id(student_id: int) -> dict:
    check_student = await StudentDAO.delete(id=student_id)
    if check_student:
        return {"message": f"Студент с ID {student_id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}