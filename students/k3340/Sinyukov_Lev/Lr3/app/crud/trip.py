from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Trip, TripParticipant
from app.schemas.trip import TripCreate, TripParticipantUpdate, TripSearchQuery, TripUpdate


def create_trip(db: Session, owner_id: int, trip_in: TripCreate) -> Trip:
    trip = Trip(owner_id=owner_id, **trip_in.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def list_trips(db: Session) -> list[Trip]:
    stmt = (
        select(Trip)
        .options(
            joinedload(Trip.owner),
            joinedload(Trip.participants).joinedload(TripParticipant.user),
        )
        .order_by(Trip.id.desc())
    )
    return list(db.scalars(stmt).unique().all())


def get_trip(db: Session, trip_id: int) -> Trip | None:
    stmt = (
        select(Trip)
        .where(Trip.id == trip_id)
        .options(
            joinedload(Trip.owner),
            joinedload(Trip.participants).joinedload(TripParticipant.user),
        )
    )
    return db.scalar(stmt)


def update_trip(db: Session, trip: Trip, trip_in: TripUpdate) -> Trip:
    for field, value in trip_in.model_dump().items():
        setattr(trip, field, value)
    db.commit()
    db.refresh(trip)
    return trip


def delete_trip(db: Session, trip: Trip) -> None:
    db.delete(trip)
    db.commit()


def add_trip_participant(db: Session, trip_id: int, user_id: int, note: str | None) -> TripParticipant:
    link = TripParticipant(trip_id=trip_id, user_id=user_id, note=note)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_participant_link(db: Session, trip_id: int, user_id: int) -> TripParticipant | None:
    return db.scalar(select(TripParticipant).where(TripParticipant.trip_id == trip_id, TripParticipant.user_id == user_id))


def update_participant_status(db: Session, link: TripParticipant, link_in: TripParticipantUpdate) -> TripParticipant:
    link.status = link_in.status
    link.note = link_in.note
    db.commit()
    db.refresh(link)
    return link


def search_trips(db: Session, query: TripSearchQuery) -> list[Trip]:
    # Manual filter composition without third-party search libraries.
    stmt = select(Trip).where(Trip.is_cancelled.is_(False))

    if query.departure_city:
        stmt = stmt.where(Trip.departure_city.ilike(f"%{query.departure_city}%"))
    if query.destination_city:
        stmt = stmt.where(Trip.destination_city.ilike(f"%{query.destination_city}%"))
    if query.start_date_from:
        stmt = stmt.where(Trip.start_date >= query.start_date_from)
    if query.start_date_to:
        stmt = stmt.where(Trip.start_date <= query.start_date_to)
    if query.max_duration_days:
        stmt = stmt.where(Trip.duration_days <= query.max_duration_days)

    stmt = stmt.options(joinedload(Trip.owner)).order_by(Trip.start_date.asc())
    return list(db.scalars(stmt).unique().all())

