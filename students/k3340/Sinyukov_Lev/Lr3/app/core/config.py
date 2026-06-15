from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Travel Buddy Finder"
    parser_service_name: str = "Travel Buddy Parser"
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/travel_buddy_db",
        validation_alias=AliasChoices("DATABASE_URL", "DB_ADMIN"),
    )
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    parser_service_url: str = "http://parser:8001"
    parser_request_timeout: int = 30
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"
    parser_user_email: str = "parser@travel-buddy.local"
    parser_username: str = "web_parser"
    parser_trip_title: str = "Web parsing results"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
