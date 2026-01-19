from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Polarify API"
    DATABASE_URL: PostgresDsn
    TEST_DATABASE_URL: PostgresDsn
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
