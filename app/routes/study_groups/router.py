from fastapi import APIRouter
from fastapi.params import Depends

from app.routes.study_groups.dao import StudyGroupDAO
from app.routes.study_groups.rb import RBStudyGroup
from app.routes.study_groups.schemas import SStudyGroupAdd, SStudyGroupGet, SStudyGroupUpdateName

router = APIRouter(
    prefix="/study_groups",
    tags=["Работа с группами", ],
)


@router.get("/", summary="Получить все группы по фильтру")
async def get_all_study_groups(request_body: RBStudyGroup = Depends()) -> list[SStudyGroupGet] | dict:
    check_group = await StudyGroupDAO.find_all(**request_body.to_dict())
    if check_group is None or len(check_group) == 0:
        return {"message": "Группы не найдены!"}
    return check_group


@router.get("/get_by_id/{study_group_id}/", summary="Получить группу по ID")
async def get_study_group_by_id(study_group_id: int) -> SStudyGroupGet | dict:
    check_group = await StudyGroupDAO.find_one_or_none_by_id(data_id=study_group_id)
    if check_group is None:
        return {"message": "Группа с заданным ID не найдена!"}
    return check_group


@router.post("/add/", summary="Добавить группу")
async def add_study_group(study_group: SStudyGroupAdd) -> dict:
    check_group = await StudyGroupDAO.add(**study_group.model_dump())
    if check_group:
        return {"message": "Группа успешно добавлена", "study_grop": study_group}
    else:
        return {"message": "Ошибка при создании группы!"}


@router.put("/update_name/", summary="Обновить название группы")
async def update_study_group_name(study_group: SStudyGroupUpdateName) -> dict:
    check_group = await StudyGroupDAO.update(
        filter_by={"id": study_group.id,},
        name=study_group.name,
    )
    if check_group:
        return {"message": f"Название группы успешно обновлено", "study_grop": study_group}
    else:
        return {"message": "Ошибка при изменении названия группы!"}


@router.delete("/delete_by_id/{study_group_id}/", summary="Удалить группу по ID")
async def delete_study_group_by_id(study_group_id: int) -> dict:
    check_group = await StudyGroupDAO.delete(id=study_group_id)
    if check_group:
        return {"message": f"Группа с ID {study_group_id} успешно удалена"}
    else:
        return {"message": "Ошибка при удалении группы!"}