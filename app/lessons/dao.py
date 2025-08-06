from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.lessons.models import Lesson


class LessonDAO(BaseDAO):
    model = Lesson

    @classmethod
    async def find_lessons(cls, **lesson_data):
        async with async_session_maker() as session:
            query = select(cls.model).options(
                joinedload(cls.model.study_group),
                joinedload(cls.model.subject),
                joinedload(cls.model.teacher),
                joinedload(cls.model.weekday),
            ).filter_by(**lesson_data)
            result = await session.execute(query)
            lessons_result = result.scalars().all()

            if lessons_result is None:
                return None

            lessons_info = []
            for lesson in lessons_result:
                lesson_dict = lesson.to_dict()
                lesson_dict["study_group"] = lesson.study_group.name
                lesson_dict["subject"] = lesson.subject.name
                lesson_dict["teacher"] = (f"{lesson.teacher.last_name} "
                                          f"{lesson.teacher.first_name} "
                                          f"{lesson.teacher.patronymic}")
                lesson_dict["weekday"] = lesson.weekday.name
                lessons_info.append(lesson_dict)

            return lessons_info

    @classmethod
    async def find_all_data(cls, lesson_id):
        async with async_session_maker() as session:
            query = select(cls.model).options(
                joinedload(cls.model.study_group),
                joinedload(cls.model.subject),
                joinedload(cls.model.teacher),
                joinedload(cls.model.weekday),
            ).filter_by(id=lesson_id)
            result = await session.execute(query)
            lesson_result = result.scalar_one_or_none()

            if lesson_result is None:
                return None

            lesson_dict = lesson_result.to_dict()
            lesson_dict["study_group"] = lesson_result.study_group.name
            lesson_dict["subject"] = lesson_result.subject.name
            lesson_dict["teacher"] = (f"{lesson_result.teacher.last_name} "
                                      f"{lesson_result.teacher.first_name} "
                                      f"{lesson_result.teacher.patronymic}")
            lesson_dict["weekday"] = lesson_result.weekday.name

            return lesson_dict