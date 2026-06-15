from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models import Message, Trip, User


def get_or_create_parser_user(db: Session) -> User:
    user = db.scalar(select(User).where(User.email == settings.parser_user_email))
    if user is not None:
        return user

    user = User(
        email=settings.parser_user_email,
        username=settings.parser_username,
        hashed_password=get_password_hash("parser-service-user"),
    )
    db.add(user)
    db.flush()
    return user


def get_or_create_parser_trip(db: Session, owner_id: int) -> Trip:
    trip = db.scalar(
        select(Trip)
        .where(Trip.owner_id == owner_id, Trip.title == settings.parser_trip_title)
        .order_by(Trip.id.asc())
    )
    if trip is not None:
        return trip

    trip = Trip(
        owner_id=owner_id,
        title=settings.parser_trip_title,
        departure_city="Internet",
        destination_city="Travel Buddy",
        start_date=date.today(),
        end_date=date.today(),
        duration_days=1,
        route_details="Parsed web page titles saved by lab3 parser.",
        is_cancelled=False,
    )
    db.add(trip)
    db.flush()
    return trip


def save_parsed_page(url: str, title: str, parser_type: str) -> dict[str, object]:
    with SessionLocal() as db:
        user = get_or_create_parser_user(db)
        trip = get_or_create_parser_trip(db, user.id)

        message = Message(
            trip_id=trip.id,
            author_id=user.id,
            content=f"[{parser_type}] {url} -> {title}",
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        return {
            "url": url,
            "title": title,
            "parser_type": parser_type,
            "trip_id": trip.id,
            "author_id": user.id,
            "message_id": message.id,
            "created_at": message.created_at.isoformat() if message.created_at else None,
        }
