from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ParseRequest(BaseModel):
    url: HttpUrl


class ParseResponse(BaseModel):
    message: str
    url: str
    title: str
    parser_type: str
    trip_id: int
    author_id: int
    message_id: int
    created_at: datetime | None = None


class ParseTaskQueuedResponse(BaseModel):
    task_id: str
    status: str
    message: str


class ParseTaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: ParseResponse | None = None
    error: str | None = None
