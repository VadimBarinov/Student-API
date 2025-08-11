from app.dao.base import BaseDAO
from app.routes.majors.models import Major


class MajorsDAO(BaseDAO):
    model = Major