from sqlalchemy import text
from app.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, relationship, mapped_column


class StudyGroup(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    students: Mapped[list["Student"]] = relationship("Student", back_populates="study_group")

    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id!r},"
                f"name={self.name!r}")

    def __repr__(self):
        return str(self)