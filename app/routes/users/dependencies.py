from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.config import get_auth_data
from app.routes.users.dao import UserDAO
from app.routes.users.models import User


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


# Функция для получения пользователя по данным из токена
async def get_current_user(token: str = Depends(get_token)):
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
    user = await UserDAO.find_one_or_none_by_id(data_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не найден")

    return user


# Функция для проверки роли администратора
async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!")