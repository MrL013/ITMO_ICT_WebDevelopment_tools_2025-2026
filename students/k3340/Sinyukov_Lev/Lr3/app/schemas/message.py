from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserRead


class MessageCreate(BaseModel):
    content: str


class MessageUpdate(BaseModel):
    content: str


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: int
    content: str
    created_at: datetime
    author: UserRead