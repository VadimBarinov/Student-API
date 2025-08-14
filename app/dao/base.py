from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None
    # Начало асинхронной функции
    # Асинхронность позволяет обрабатывать несколько запросов одновременно, не блокируя другие операции
    @classmethod
    # Принимает неограниченное количество именованных аргументов
    async def find_all(cls, session: AsyncSession, **filter_by):
        # query = text("""
        #     SELECT * FROM students;
        # """)
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    # Поиск по ID
    # Вернет None, если ничего не нашел
    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalars().first()

    # Поиск по фильтру
    # Фильтр передается в виде списка именованных аргументов
    # Вернет None, если ничего не нашел
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().first()

    # Метод для добавления новой записи в таблицу
    @classmethod
    async def add(cls, session: AsyncSession, **values):
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

    # Метод для изменения поля таблицы
    @classmethod
    async def update(cls, session: AsyncSession, filter_by, **values):
        # Запрос на обновление записей
        query = (
            sqlalchemy_update(cls.model)
            # Добавляются условия фильтрации, чтобы обновить только те записи,
            # которые соответствуют заданным условиям
            .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
            # Устанавливаются новые значения для обновляемых записей
            .values(**values)
            # Опция, чтобы синхронизировать состояние сессии с базой данных после выполнения запроса
            .execution_options(synchronize_session="fetch")
        )
        # Выполнение запроса
        result = await session.execute(query)
        try:
            # Сохранение изменений в базе данных
            await session.commit()
        except SQLAlchemyError as e:
            # Транзакция откатывается, если возникает ошибка
            await session.rollback()
            raise e
        # Возвращает количество обновленных строк
        return result.rowcount

    # Метод для удаления
    @classmethod
    async def delete(cls,session: AsyncSession, delete_all: bool = False, **filter_by):
        # Проверка на наличие параметров
        if delete_all == False and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        if delete_all:
            query = sqlalchemy_delete(cls.model)
        else:
            query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount