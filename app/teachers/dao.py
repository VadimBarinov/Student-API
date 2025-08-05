from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.teachers.models import Teacher


class TeacherDAO(BaseDAO):
    model = Teacher

    @classmethod
    async def find_teachers(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(**filter_by)
            result = await session.execute(query)
            teachers_info = result.scalars().all()

            teachers_data = []
            for teacher in teachers_info:
                teacher_dict = teacher.to_dict()
                teacher_dict["major"] = teacher.major.name
                teachers_data.append(teacher_dict)

            return teachers_data


    @classmethod
    async def find_full_data(cls, teacher_id):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=teacher_id)
            result = await session.execute(query)
            teacher_info = result.scalar_one_or_none()

            if teacher_info is None:
                return None

            teacher_dict = teacher_info.to_dict()
            teacher_dict["major"] = teacher_info.major.name

            return teacher_dict

