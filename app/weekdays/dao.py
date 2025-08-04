from app.dao.base import BaseDAO
from app.weekdays.models import Weekday


class WeekdayDAO(BaseDAO):
    model = Weekday