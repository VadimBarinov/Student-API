from sqlalchemy import select, update, event, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.majors.models import Major
from app.students.models import Student
from app.dao.base import BaseDAO


@event.listens_for(Student, "after_insert")
def receive_after_insert(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students + 1)
    )


@event.listens_for(Student, 'after_delete')
def receive_after_delete(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students - 1)
    )


class StudentDAO(BaseDAO):
    model = Student

    # Метод для получения списка всех студентов по фильтру
    @classmethod
    async def find_students(cls, **student_data):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(**student_data)
            result = await session.execute(query)
            students_info = result.scalars().all()

            students_data = []
            for student in students_info:
                student_dict = student.to_dict()
                student_dict["major"] = student.major.major_name
                students_data.append(student_dict)

            return students_data


    # Метод для получения полной информации о студенте
    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            # Получение информации о студенте
            # Позволяет избежать второго запроса, благодаря joinedload()
            query_student = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result_student = await session.execute(query_student)
            student_info = result_student.scalar_one_or_none()

            if student_info is None:
                return None

            # Добавляем название специальности
            student_data = student_info.to_dict()
            student_data['major'] = student_info.major.major_name

            return student_data

    # Метод для добавления студентов
    @classmethod
    async def add_student(cls, **student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = cls.model(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return new_student_id

    # Метод для удаления студента по id
    @classmethod
    async def delete_student_by_id(cls, student_id):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(id=student_id)
                result = await session.execute(query)

                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return result.rowcount
