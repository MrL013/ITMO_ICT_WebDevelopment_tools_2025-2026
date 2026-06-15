from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.trip_participant import ParticipantStatus
from app.schemas.user import UserRead


class TripBase(BaseModel):
    title: str
    departure_city: str
    destination_city: str
    start_date: date
    end_date: date
    duration_days: int
    route_details: str | None = None


class TripCreate(TripBase):
    pass


class TripUpdate(TripBase):
    is_cancelled: bool = False


class TripParticipantCreate(BaseModel):
    note: str | None = None


class TripParticipantUpdate(BaseModel):
    status: ParticipantStatus
    note: str | None = None


class TripParticipantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: ParticipantStatus
    note: str | None
    joined_at: datetime
    user: UserRead


class TripRead(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    is_cancelled: bool
    created_at: datetime


class TripReadDetailed(TripRead):
    owner: UserRead
    participants: list[TripParticipantRead]


class TripSearchQuery(BaseModel):
    departure_city: str | None = None
    destination_city: str | None = None
    start_date_from: date | None = None
    start_date_to: date | None = None
    max_duration_days: int | None = None

