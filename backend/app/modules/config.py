import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    API_version_string: str = "/api/v1/"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = ""
    ALGORITHM: str = "HS256"


settings = Settings()
