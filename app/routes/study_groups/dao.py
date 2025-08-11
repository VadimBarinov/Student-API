from app.dao.base import BaseDAO
from app.routes.study_groups.models import StudyGroup


class StudyGroupDAO(BaseDAO):
    model = StudyGroup