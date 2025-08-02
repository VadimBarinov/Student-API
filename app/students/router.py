from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent, SStudentAdd

# Создание роутера
# prefix устанавливает префикс для всех маршрутов роутера
# tags добавляет тег роутеру, будет использоваться в документации
router = APIRouter(
    prefix="/students", tags=["Работа со студентами", ]
)


# эндпоинт роутер для получения всех студентов
# summary это описание, будет показываться в документации
@router.get("/", summary="Получить всех студентов")
# Начало асинхронной функции
# Асинхронность позволяет обрабатывать несколько запросов одновременно, не блокируя другие операции
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
        return await StudentDAO.find_students(**request_body.to_dict())


# получение студента по id
@router.get("/{id}/", summary="Получить одного студента по ID")
async def get_student_by_id(student_id: int) -> SStudent | dict:
    result = await StudentDAO.find_full_data(student_id)
    # Обработчик None
    if result is None:
        return {"message": f"Студент с ID {student_id} не найден!"}
    return result


# Получение студента с учетом переданного фильтра
# Используется Request Body Student из rb.py
@router.get("/by_filter/", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudent | dict:
    result = await StudentDAO.find_one_or_none(**request_body.to_dict())
    # Обработчик None
    if result is None:
        return {"message": f"Студент с указанными вами параметрами не найден!"}
    return result


@router.post("/add/", summary="Добавить нового студента")
async def add_student(student: SStudentAdd) -> dict:
    check_student = await StudentDAO.add_student(**student.model_dump())
    if check_student:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}


@router.delete("/delete/{id}/", summary="Удаление студента по ID")
async def delete_student_by_id(student_id: int) -> dict:
    check_student = await StudentDAO.delete_student_by_id(student_id=student_id)
    if check_student:
        return {"message": f"Студент с ID {student_id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}

# ----------------------------------------------------------------------------------
# Нужно добавить эндпоинты:
# PUT на изменение записи
# ----------------------------------------------------------------------------------