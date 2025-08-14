from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.routes.teachers.models import Teacher


class TeacherDAO(BaseDAO):
    model = Teacher

    @classmethod
    async def find_teachers(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).options(joinedload(cls.model.major)).filter_by(**filter_by)
        result = await session.execute(query)
        teachers_info = result.scalars().all()

        teachers_data = []
        for teacher in teachers_info:
            teacher_dict = teacher.to_dict()
            teacher_dict["major"] = teacher.major.major_name
            teachers_data.append(teacher_dict)

        return teachers_data


    @classmethod
    async def find_full_data(cls, session: AsyncSession, teacher_id):
        query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=teacher_id)
        result = await session.execute(query)
        teacher_info = result.scalar_one_or_none()

        if teacher_info is None:
            return None

        teacher_dict = teacher_info.to_dict()
        teacher_dict["major"] = teacher_info.major.major_name

        return teacher_dict

