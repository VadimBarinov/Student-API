from fastapi import APIRouter, Depends
from app.routes.subjects.dao import SubjectDAO
from app.routes.subjects.rb import RBSubject
from app.routes.subjects.schemas import SSubjectGet, SSubjectAdd, SSubjectUpdateName

router = APIRouter(
    prefix="/subjects",
    tags=["Работа с учебными предметами", ],
)


@router.get("/", summary="Получить все предметы по фильтру")
async def get_all_subjects_by_filter(subject: RBSubject = Depends()) -> list[SSubjectGet] | dict:
    check_subjects = await SubjectDAO.find_all(**subject.to_dict())
    if check_subjects is None or len(check_subjects) == 0:
        return {"message": f"Предметы не найдены!"}
    return check_subjects


@router.get("/get_by_id/{subject_id}/", summary="Получить предмет по ID")
async def get_subjects_by_id(subject_id: int) -> SSubjectGet | dict:
    check_subject = await SubjectDAO.find_one_or_none_by_id(data_id=subject_id)
    if check_subject is None:
        return {"message": f"Предмет с ID {subject_id} не найден!"}
    return check_subject


@router.post("/add/", summary="Добавить новый предмет")
async def add_new_subject(subject: SSubjectAdd) -> dict:
    check_subject = await SubjectDAO.add(**subject.model_dump())
    if check_subject:
        return {"message": "Предмет успешно добавлен!", "subject": subject}
    else:
        return {"message": "Ошибка при добавлении предмета"}


@router.put("/update_name/", summary="Обновить название предмета")
async def update_subject_name(subject: SSubjectUpdateName) -> dict:
    check_subject = await SubjectDAO.update(
        filter_by={"id": subject.id},
        name=subject.name,
    )
    if check_subject:
        return {"message": "Название предмета успешно обновлено!", "subject": subject}
    else:
        return {"message": "Ошибка при обновлении названия предмета!"}


@router.delete("/delete/{subject_id}/", summary="Удалить предмет по ID")
async def delete_subject_by_id(subject_id: int) -> dict:
    check_subject = await SubjectDAO.delete(id=subject_id)
    if check_subject:
        return {"message": f"Предмет с ID {subject_id} успешно удален!"}
    else:
        return {"message": "Ошибка при удалении предмета!"}