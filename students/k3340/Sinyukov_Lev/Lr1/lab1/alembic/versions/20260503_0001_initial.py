"""initial schema

Revision ID: 20260503_0001
Revises: None
Create Date: 2026-05-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260503_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


participant_status_enum = sa.Enum("requested", "approved", "rejected", name="participantstatus")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.Column("travel_preferences", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_profiles_id"), "profiles", ["id"], unique=False)

    op.create_table(
        "trips",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("departure_city", sa.String(length=100), nullable=False),
        sa.Column("destination_city", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("route_details", sa.Text(), nullable=True),
        sa.Column("is_cancelled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trips_departure_city"), "trips", ["departure_city"], unique=False)
    op.create_index(op.f("ix_trips_destination_city"), "trips", ["destination_city"], unique=False)
    op.create_index(op.f("ix_trips_end_date"), "trips", ["end_date"], unique=False)
    op.create_index(op.f("ix_trips_id"), "trips", ["id"], unique=False)
    op.create_index(op.f("ix_trips_owner_id"), "trips", ["owner_id"], unique=False)
    op.create_index(op.f("ix_trips_start_date"), "trips", ["start_date"], unique=False)

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_author_id"), "messages", ["author_id"], unique=False)
    op.create_index(op.f("ix_messages_id"), "messages", ["id"], unique=False)
    op.create_index(op.f("ix_messages_trip_id"), "messages", ["trip_id"], unique=False)

    op.create_table(
        "trip_participants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", participant_status_enum, nullable=False),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trip_id", "user_id", name="uq_trip_user"),
    )
    op.create_index(op.f("ix_trip_participants_id"), "trip_participants", ["id"], unique=False)
    op.create_index(op.f("ix_trip_participants_trip_id"), "trip_participants", ["trip_id"], unique=False)
    op.create_index(op.f("ix_trip_participants_user_id"), "trip_participants", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_trip_participants_user_id"), table_name="trip_participants")
    op.drop_index(op.f("ix_trip_participants_trip_id"), table_name="trip_participants")
    op.drop_index(op.f("ix_trip_participants_id"), table_name="trip_participants")
    op.drop_table("trip_participants")
    op.drop_index(op.f("ix_messages_trip_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_author_id"), table_name="messages")
    op.drop_table("messages")

    op.drop_index(op.f("ix_trips_start_date"), table_name="trips")
    op.drop_index(op.f("ix_trips_owner_id"), table_name="trips")
    op.drop_index(op.f("ix_trips_id"), table_name="trips")
    op.drop_index(op.f("ix_trips_end_date"), table_name="trips")
    op.drop_index(op.f("ix_trips_destination_city"), table_name="trips")
    op.drop_index(op.f("ix_trips_departure_city"), table_name="trips")
    op.drop_table("trips")

    op.drop_index(op.f("ix_profiles_id"), table_name="profiles")
    op.drop_table("profiles")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
