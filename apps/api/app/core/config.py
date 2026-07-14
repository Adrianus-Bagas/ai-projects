from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Workspace API"
    APP_VERSION: str = "0.1.0"

    API_PREFIX: str = "/api/v1"

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()