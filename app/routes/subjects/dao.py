from app.dao.base import BaseDAO
from app.routes.subjects.models import Subject


class SubjectDAO(BaseDAO):
    model = Subject