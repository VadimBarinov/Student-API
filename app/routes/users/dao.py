from app.dao.base import BaseDAO
from app.routes.users.models import User


class UserDAO(BaseDAO):
    model = User