from datetime import timezone, datetime, timedelta

from asyncpg.pgproto.pgproto import timedelta
from passlib.context import CryptContext
from jose import jwt
from app.config import get_auth_data


# Создает JWT
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # Принимает словарь с данными и добавляет время истечения токена (30 дней)
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    # Кодирует данные в JWT с использованием секретного ключа и алгоритма шифрования
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    return encode_jwt


# Создание контекста для хэширования паролей
# Используется алгоритм bcrypt
# Параметр deprecated="auto" указывает использовать рекомендованные схемы хэширования и автоматически обновлять устаревшие
pwd_context = CryptContext(schemes=["bcrypt"], deprecateted="auto")


# Создание хэша пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Проверка хэша пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)