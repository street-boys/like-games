from functools import lru_cache

from pydantic import BaseSettings


class AdminSettings(BaseSettings):
    ADMIN_INFINITY_ACCESS_TOKEN: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class DatabaseSettings(BaseSettings):
    USER_DATABASE_URI: str = "sqlite+aiosqlite:///user.db"


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str


@lru_cache()
def get_jwt_settings() -> JWTSettings:
    return JWTSettings()


class TelegramSettings(BaseSettings):
    TELEGRAM_BOT_API_TOKEN: str


@lru_cache()
def get_telegram_settings() -> TelegramSettings:
    return TelegramSettings()
