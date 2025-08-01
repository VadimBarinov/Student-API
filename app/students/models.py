from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date
from app.majors.models import Major


# Модель Student для описания студента
class Student(Base):
    # В некоторых полях класса используются аннотации, сформированные в файле database.py
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    enrollment_year: Mapped[int]
    course: Mapped[int]
    special_notes: Mapped[str_null_true]
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=False)

    # Foreign Key. В качестве внешнего ключа используется поле id модели Major
    # Определяем отношения: один студент имеет один факультет
    major: Mapped["Major"] = relationship("Major", back_populates="students")

    # Метод для корректного отображения объекта класса в качестве строки
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    # Возвращает строковое представление объекта
    def __repr__(self):
        return str(self)

    # Метод преобразует все полученные данные в обычный словарь
    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "address": self.address,
            "enrollment_year": self.enrollment_year,
            "course": self.course,
            "special_notes": self.special_notes,
            "major_id": self.major_id,
        }
