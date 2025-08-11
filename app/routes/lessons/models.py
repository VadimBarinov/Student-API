from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.database import Base, int_pk


class Lesson(Base):
    id: Mapped[int_pk]
    study_group_id: Mapped[int] = mapped_column(ForeignKey("studygroups.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    weekday_id: Mapped[int] = mapped_column(ForeignKey("weekdays.id"), nullable=False)
    lesson_number: Mapped[int]
    auditorium: Mapped[str]

    study_group: Mapped["StudyGroup"] = relationship("StudyGroup", back_populates="lessons")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="lessons")
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="lessons")
    weekday: Mapped["Weekday"] = relationship("Weekday", back_populates="lessons")

    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id},"
                f"study_group_id={self.study_group_id},"
                f"subject_id={self.subject_id},"
                f"teacher_id={self.teacher_id},"
                f"weekday_id={self.weekday_id},"
                f"lesson_number={self.lesson_number},"
                f"auditorium={self.auditorium})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "study_group_id": self.study_group_id,
            "subject_id": self.subject_id,
            "teacher_id": self.teacher_id,
            "weekday_id": self.weekday_id,
            "lesson_number": self.lesson_number,
            "auditorium": self.auditorium,
        }