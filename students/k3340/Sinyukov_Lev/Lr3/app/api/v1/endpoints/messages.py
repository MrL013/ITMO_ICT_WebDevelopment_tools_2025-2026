from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.message import create_message, delete_message, get_message, list_messages_for_trip, update_message
from app.crud.trip import get_trip
from app.models import User
from app.schemas.message import MessageCreate, MessageRead, MessageUpdate

router = APIRouter(prefix="/trips/{trip_id}/messages", tags=["messages"])


@router.get("/", response_model=list[MessageRead])
def list_messages(trip_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[MessageRead]:
    if get_trip(db, trip_id) is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    messages = list_messages_for_trip(db, trip_id)
    return [MessageRead.model_validate(message) for message in messages]


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def create_message_endpoint(
    trip_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageRead:
    if get_trip(db, trip_id) is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    message = create_message(db, trip_id, current_user.id, data.content)
    message = get_message(db, message.id)
    assert message is not None
    return MessageRead.model_validate(message)


@router.put("/{message_id}", response_model=MessageRead)
def update_message_endpoint(
    trip_id: int,
    message_id: int,
    data: MessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageRead:
    message = get_message(db, message_id)
    if message is None or message.trip_id != trip_id:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only author can edit message")
    updated = update_message(db, message, data)
    updated = get_message(db, updated.id)
    assert updated is not None
    return MessageRead.model_validate(updated)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_endpoint(
    trip_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    message = get_message(db, message_id)
    if message is None or message.trip_id != trip_id:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only author can delete message")
    delete_message(db, message)

