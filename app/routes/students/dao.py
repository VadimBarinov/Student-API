from sqlalchemy import select, update, event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.routes.majors.models import Major
from app.routes.students.models import Student
from app.dao.base import BaseDAO
from app.routes.study_groups.models import StudyGroup


@event.listens_for(Student, "after_insert")
def receive_after_insert(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students + 1)
    )
    study_group_id = target.study_group_id
    connection.execute(
        update(StudyGroup)
        .where(StudyGroup.id == study_group_id)
        .values(count_students=StudyGroup.count_students + 1)
    )


@event.listens_for(Student, "after_delete")
def receive_after_delete(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students - 1)
    )
    study_group_id = target.study_group_id
    connection.execute(
        update(StudyGroup)
        .where(StudyGroup.id == study_group_id)
        .values(count_students=StudyGroup.count_students - 1)
    )


class StudentDAO(BaseDAO):
    model = Student

    # Метод для получения списка всех студентов по фильтру
    @classmethod
    async def find_students(cls, session: AsyncSession, **student_data):
        query = select(cls.model).options(
            joinedload(cls.model.major), joinedload(cls.model.study_group)
        ).filter_by(**student_data)
        result = await session.execute(query)
        students_info = result.scalars().all()

        students_data = []
        for student in students_info:
            student_dict = student.to_dict()
            student_dict["major"] = student.major.major_name
            student_dict["study_group"] = student.study_group.name
            students_data.append(student_dict)

        return students_data


    # Метод для получения полной информации о студенте
    @classmethod
    async def find_full_data(cls, session: AsyncSession, student_id: int):
        # Получение информации о студенте
        # Позволяет избежать второго запроса, благодаря joinedload()
        query_student = select(cls.model).options(
            joinedload(cls.model.major), joinedload(cls.model.study_group)
        ).filter_by(id=student_id)
        result_student = await session.execute(query_student)
        student_info = result_student.scalar_one_or_none()

        if student_info is None:
            return None

        # Добавляем название специальности
        student_data = student_info.to_dict()
        student_data["major"] = student_info.major.major_name
        student_data["study_group"] = student_info.study_group.name

        return student_data
