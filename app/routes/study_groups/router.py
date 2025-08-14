from fastapi import APIRouter, HTTPException, status

from app.dependencies import SessionDep
from app.routes.study_groups.dao import StudyGroupDAO
from app.routes.study_groups.rb import RBStudyGroupDep
from app.routes.study_groups.schemas import SStudyGroupAdd, SStudyGroupGet, SStudyGroupUpdateName

router = APIRouter(
    prefix="/study_groups",
    tags=["Работа с группами", ],
)


@router.get("/", summary="Получить все группы по фильтру")
async def get_all_study_groups(session: SessionDep, request_body: RBStudyGroupDep) -> list[SStudyGroupGet] | dict:
    check_group = await StudyGroupDAO.find_all(session=session, **request_body.to_dict())
    if check_group is None or len(check_group) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Группы не найдены!")
    return check_group


@router.get("/get_by_id/{study_group_id}/", summary="Получить группу по ID")
async def get_study_group_by_id(session: SessionDep, study_group_id: int) -> SStudyGroupGet | dict:
    check_group = await StudyGroupDAO.find_one_or_none_by_id(session=session, data_id=study_group_id)
    if check_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Группа с ID {study_group_id} не найдена!")
    return check_group


@router.post("/add/", summary="Добавить группу")
async def add_study_group(session:SessionDep, study_group: SStudyGroupAdd) -> dict:
    check_group = await StudyGroupDAO.add(session=session, **study_group.model_dump())
    if check_group:
        return {"message": "Группа успешно добавлена", "study_grop": study_group}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при создании группы!")


@router.put("/update_name/", summary="Обновить название группы")
async def update_study_group_name(session: SessionDep, study_group: SStudyGroupUpdateName) -> dict:
    check_group = await StudyGroupDAO.update(
        session=session,
        filter_by={"id": study_group.id,},
        name=study_group.name,
    )
    if check_group:
        return {"message": f"Название группы успешно обновлено", "study_grop": study_group}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при изменении названия группы!")


@router.delete("/delete_by_id/{study_group_id}/", summary="Удалить группу по ID")
async def delete_study_group_by_id(session: SessionDep, study_group_id: int) -> dict:
    check_group = await StudyGroupDAO.delete(session=session, id=study_group_id)
    if check_group:
        return {"message": f"Группа с ID {study_group_id} успешно удалена"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при удалении группы!")
