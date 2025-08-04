from app.dao.base import BaseDAO
from app.study_groups.models import StudyGroup


class StudyGroupDAO(BaseDAO):
    model = StudyGroup