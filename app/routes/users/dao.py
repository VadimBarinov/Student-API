from sqlalchemy import update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.routes.users.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_or_delete_role(cls, session: AsyncSession, user_id: int, role_name: str, new_value):

        if not hasattr(cls.model, role_name):
            return None

        query = update(cls.model).filter_by(id=user_id).values(
            **{role_name: new_value}
        ).execution_options(synchronize_session="fetch")
        result = await session.execute(query)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return result.rowcount
