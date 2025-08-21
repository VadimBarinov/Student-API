from datetime import timezone, datetime, timedelta
from asyncpg.pgproto.pgproto import timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from passlib.exc import InvalidTokenError
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_auth_data
from app.routes.users.dao import UserDAO


class RefreshTokenSystem:
    def __init__(self):
        auth_data = get_auth_data()
        self.secret = auth_data["secret_key"]
        self.algorithm = auth_data["algorithm"]
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.access_token_expire = timedelta(minutes=1)
        self.refresh_token_expire = timedelta(minutes=2)

    def create_token_pair(self, user_id: int):
        """Создание пары access и refresh токенов"""
        now = datetime.now(timezone.utc)

        # Access токен (короткий срок жизни)
        access_payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": now + self.access_token_expire,
            "iat": now,
        }
        access_token = jwt.encode(claims=access_payload, key=self.secret, algorithm=self.algorithm)

        # Refresh токен (длинный срок жизни)
        refresh_payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": now + self.refresh_token_expire,
            "iat": now,
        }
        refresh_token = jwt.encode(claims=refresh_payload, key=self.secret, algorithm=self.algorithm)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": int(self.access_token_expire.total_seconds())
        }

    def refresh_access_token(self, refresh_token):
        """Обновление access токена с помощью refresh токена"""
        try:
            payload = jwt.decode(token=refresh_token, key=self.secret, algorithms=[self.algorithm, ])

            if payload.get("type") != "refresh":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Не refresh токен!")

            user_id = int(payload.get("sub"))
            return self.create_token_pair(user_id=user_id)

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Refresh токен истёк")
        except InvalidTokenError:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Недействительный access токен")

    def get_password_hash(self, password: str) -> str:
        """Создание хэша пароля"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка хэша пароля"""
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, session: AsyncSession, email: EmailStr, password: str):
        """Авторизация пользователя"""
        # Получаем пользователя по E-mail
        user = await UserDAO.find_one_or_none(session=session, email=email)
        # Проверяем на существование и на совпадение пароля
        if not user or self.verify_password(plain_password=password, hashed_password=user.password) is False:
            return None
        return user
