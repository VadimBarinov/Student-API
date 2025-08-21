from typing import Annotated

from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from passlib.exc import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_auth_data
from app.database import async_session_maker
from app.routes.users.dao import UserDAO
from app.routes.users.schemas import SUserGet


async def get_session():
    """Получение сессии БД"""
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_access_token(request: Request):
    """Получение access токена"""
    token = request.cookies.get("access_token")
    if not token:
        # Выброс ошибки, если токен не найден
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не найден")
    return token

AccessTokenDep = Annotated[str, Depends(get_access_token)]


def get_refresh_token(request: Request):
    """Получение refresh токена"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        # Выброс ошибки, если токен не найден
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не найден")
    return refresh_token

RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]


async def get_current_user(session: SessionDep, token: AccessTokenDep) -> SUserGet:
    """Получение пользователя по данным из токена"""
    try:
        # Получаем секретный ключ и алгоритм из файла с конфигом
        auth_data = get_auth_data()
        # Декодируем токен
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
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

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен истек")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Недействительный access токен")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не валидный!")


CurrentUser = Annotated[SUserGet, Depends(get_current_user)]


async def get_current_admin_user(current_user: CurrentUser) -> SUserGet:
    """Проверка роли администратора"""
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!")

CurrentAdminUser = Annotated[SUserGet, Depends(get_current_admin_user)]
