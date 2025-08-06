from sqlalchemy.orm import Mapped, relationship
from app.database import Base, int_pk, str_uniq


class Subject(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="subject")


    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id},"
                f"name={self.name})")

    def __repr__(self):
        return str(self)
