from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text
from app.database import Base, int_pk, str_uniq, str_null_true


# Модель Major для описания направления обучения
class Major(Base):
    # В некоторых полях класса используются аннотации, сформированные в файле database.py
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    # Определяем отношения: один факультет может иметь много студентов
    students: Mapped[list["Student"]] = relationship("Student", back_populates="major")
    teachers: Mapped[list["Teacher"]] = relationship("Teacher", back_populates="major")

    # Метод для корректного отображения объекта класса в качестве строки
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"

    # Возвращает строковое представление объекта
    def __repr__(self):
        return str(self)