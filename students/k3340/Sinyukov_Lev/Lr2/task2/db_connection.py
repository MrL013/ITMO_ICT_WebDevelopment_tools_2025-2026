from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/travel_buddy_db",
        validation_alias=AliasChoices("DATABASE_URL", "DB_ADMIN"),
    )
    parser_user_email: str = "parser@travel-buddy.local"
    parser_username: str = "web_parser"
    parser_trip_title: str = "Web parsing results"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    return SessionLocal()


def get_or_create_parser_user_sql() -> str:
    return """
    INSERT INTO users (email, username, hashed_password, created_at)
    VALUES (:email, :username, :hashed_password, NOW())
    ON CONFLICT (email) DO UPDATE SET email = EXCLUDED.email
    RETURNING id
    """


def get_parser_trip_id_sql() -> str:
    return """
    SELECT id
    FROM trips
    WHERE owner_id = :owner_id AND title = :title
    ORDER BY id
    LIMIT 1
    """


def get_create_parser_trip_sql() -> str:
    return """
    INSERT INTO trips (
        owner_id,
        title,
        departure_city,
        destination_city,
        start_date,
        end_date,
        duration_days,
        route_details,
        is_cancelled,
        created_at
    )
    VALUES (
        :owner_id,
        :title,
        :departure_city,
        :destination_city,
        CURRENT_DATE,
        CURRENT_DATE,
        1,
        :route_details,
        FALSE,
        NOW()
    )
    RETURNING id
    """


def get_insert_message_sql() -> str:
    return """
    INSERT INTO messages (trip_id, author_id, content, created_at)
    VALUES (:trip_id, :author_id, :content, :created_at)
    """
