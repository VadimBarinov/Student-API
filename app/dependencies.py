from typing import Annotated

from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_auth_data
from app.database import async_session_maker
from app.routes.users.dao import UserDAO
from app.routes.users.schemas import SUserGet


async def get_session():
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Функция для получение токена из куки
def get_token(request: Request):
    # Получение токена
    token = request.cookies.get("user_access_token")
    # Проверка на существование
    if not token:
        # Выброс ошибки, если токен не найден
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Токен не найден')
    return token

TokenDep = Annotated[str, Depends(get_token)]


# Функция для получения пользователя по данным из токена
async def get_current_user(session: SessionDep, token: TokenDep) -> SUserGet:
    # Декодер для получения данных из токена (exp, sub)
    try:
        # Получаем секретный ключ и алгоритм из файла с конфигом
        auth_data = get_auth_data()
        # Декодируем токен
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
    except JWTError:
        # Выброс ошибки, если токен не найден
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не валидный!")

    # Получение срока токена
    expire = payload.get("exp")
    # Преобразование в нужный формат
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

    # Условие для проверки срока токена
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Токен истек')

    # Получение ID пользователя
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Не найден ID пользователя")

    # Получение самого пользователя по ID
    user = await UserDAO.find_one_or_none_by_id(session=session, data_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не найден")

    return user

CurrentUser = Annotated[SUserGet, Depends(get_current_user)]


# Функция для проверки роли администратора
async def get_current_admin_user(current_user: CurrentUser) -> SUserGet:
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!")

CurrentAdminUser = Annotated[SUserGet, Depends(get_current_admin_user)]
