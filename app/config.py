import os
from pydantic_settings import BaseSettings, SettingsConfigDict


# Класс для настроек подключения к БД
# Наследуется от класса BaseSettings модуля pydentic_settings
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    # Указывается путь на файл .env
    # В нем хранятся параметры подключения к БД
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


# Функция для получения URL для подключения к БД
# Используется в database.py
def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

def get_auth_data():
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
    }