from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Message
from app.schemas.message import MessageUpdate


def create_message(db: Session, trip_id: int, author_id: int, content: str) -> Message:
    message = Message(trip_id=trip_id, author_id=author_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_messages_for_trip(db: Session, trip_id: int) -> list[Message]:
    stmt = (
        select(Message)
        .where(Message.trip_id == trip_id)
        .options(joinedload(Message.author))
        .order_by(Message.created_at.asc())
    )
    return list(db.scalars(stmt).unique().all())


def get_message(db: Session, message_id: int) -> Message | None:
    stmt = select(Message).where(Message.id == message_id).options(joinedload(Message.author))
    return db.scalar(stmt)


def update_message(db: Session, message: Message, data: MessageUpdate) -> Message:
    message.content = data.content
    db.commit()
    db.refresh(message)
    return message


def delete_message(db: Session, message: Message) -> None:
    db.delete(message)
    db.commit()