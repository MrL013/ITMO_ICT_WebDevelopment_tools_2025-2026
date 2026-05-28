from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ParticipantStatus(str, Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"


class TripParticipant(Base):
    __tablename__ = "trip_participants"
    __table_args__ = (UniqueConstraint("trip_id", "user_id", name="uq_trip_user"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[ParticipantStatus] = mapped_column(SqlEnum(ParticipantStatus), default=ParticipantStatus.requested, nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    trip = relationship("Trip", back_populates="participants")
    user = relationship("User", back_populates="trip_links")

