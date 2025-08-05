from sqlalchemy.orm import Mapped
from app.database import Base, int_pk, str_uniq


class Subject(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]


    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id},"
                f"name={self.name})")

    def __repr__(self):
        return str(self)
