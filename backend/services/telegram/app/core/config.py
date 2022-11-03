from functools import lru_cache

from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    TELEGRAM_DATABASE_URL: str = 'sqlite://telegram.db'


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class SiteSettings(BaseSettings):
    AUTH_SITE_BASE_URL: str = 'http://localhost'
    POT_SITE_BASE_URL: str = 'http://localhost'


@lru_cache()
def get_site_settings() -> SiteSettings:
    return SiteSettings()


class TelegramSettings(BaseSettings):
    TELEGRAM_BOT_API_TOKEN: str


@lru_cache()
def get_telegram_settings() -> TelegramSettings:
    return TelegramSettings()
