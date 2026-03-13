from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс настроек"""
    APP_NAME: str
    ENV: str

    JWT_SECRET: str
    JWT_ALG: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # База данных
    SQLITE_PATH: str

    # OpenRouter настройки
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_SITE_URL: str
    OPENROUTER_APP_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Инициализация: Pydantic пойдет в .env и заполнит все поля выше.
settings = Settings()