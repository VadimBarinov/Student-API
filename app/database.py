from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped

from app.config import get_db_url


# url для подключения к базе данных
DATABASE_URL = get_db_url()


# Создание движка
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Настройка аннотаций
# Чтобы не было повторов кода
# Далее буду использоваться при создании полей моделей
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


# Базовый класс
# От него будут наследоваться все модели
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # Название таблицы генерируется автоматически, берется из названия класса
    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower()}s"

    # РАСШИРЕНИЕ КЛАССА
    # Дата и время создания записи.
    # Описанная аннотация сделает так, чтоб на стороне базы данных вытягивалась дата с сервера,
    # на котором база данных размещена: server_default=func.now().
    created_at: Mapped[created_at]
    # колонка, в которой будет фиксироваться текущая дата и время после обновления.
    updated_at: Mapped[updated_at]