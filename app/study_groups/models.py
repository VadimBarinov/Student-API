from sqlalchemy import ForeignKey

from app.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped


class StudyGroup(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id!r},"
                f"name={self.name!r}")

    def __repr__(self):
        return str(self)