from app.dao.base import BaseDAO
from app.routes.weekdays.models import Weekday


class WeekdayDAO(BaseDAO):
    model = Weekday