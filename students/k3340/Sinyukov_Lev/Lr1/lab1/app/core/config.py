from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Travel Buddy Finder"
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/travel_buddy_db",
        validation_alias=AliasChoices("DATABASE_URL", "DB_ADMIN"),
    )
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()