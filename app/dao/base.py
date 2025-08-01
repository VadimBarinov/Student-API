from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    model = None
    # Начало асинхронной функции
    # Асинхронность позволяет обрабатывать несколько запросов одновременно, не блокируя другие операции
    @classmethod
    # Принимает неограниченное количество именованных аргументов
    async def find_all(cls, **filter_by):
        # Создание сессии
        # Закроется автоматически после завершения действий
        async with async_session_maker() as session:
            # query = text("""
            #     SELECT * FROM students;
            # """)
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    # Поиск по ID
    # Вернет None, если ничего не нашел
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Поиск по фильтру
    # Фильтр передается в виде списка именованных аргументов
    # Вернет None, если ничего не нашел
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Метод для добавления новой записи в таблицу
    @classmethod
    async def add(cls, **values):
        # Создаем асинхронную сессию
        async with async_session_maker() as session:
            # Начинаем транзакцию
            async with session.begin():
                # Создаем новый экземпляр модели
                new_instance = cls.model(**values)
                # Добавляем новый экземпляр в сессию
                session.add(new_instance)
                try:
                    # Пытаемся зафиксировать изменения в БД
                    await session.commit()
                except SQLAlchemyError as e:
                    # В случае ошибки откатываем транзакцию и пробрасываем исключение дальше
                    await session.rollback()
                    raise e
                # Возвращаем созданный экземпляр.
                return new_instance