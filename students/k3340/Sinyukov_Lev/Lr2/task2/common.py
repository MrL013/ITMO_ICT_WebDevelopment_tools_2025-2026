from __future__ import annotations

from datetime import datetime
from html.parser import HTMLParser
from urllib.request import Request, urlopen

from sqlalchemy import text
from sqlalchemy.orm import Session

from db_connection import (
    get_create_parser_trip_sql,
    get_insert_message_sql,
    get_or_create_parser_user_sql,
    get_parser_trip_id_sql,
    get_session,
    settings,
)

REQUEST_TIMEOUT = 10
URLS = [
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://docs.python.org/3/",
    "https://www.djangoproject.com/",
    "https://palletsprojects.com/",
]


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_title = False
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self._parts.append(data.strip())

    @property
    def title(self) -> str:
        return " ".join(part for part in self._parts if part).strip()


def split_into_chunks(items: list[str], parts: int) -> list[list[str]]:
    if parts <= 0:
        raise ValueError("parts must be greater than zero")

    chunk_count = min(parts, len(items))
    base_size, remainder = divmod(len(items), chunk_count)
    chunks: list[list[str]] = []
    start = 0

    for index in range(chunk_count):
        extra = 1 if index < remainder else 0
        end = start + base_size + extra
        chunks.append(items[start:end])
        start = end

    return chunks


def extract_title(html: str) -> str:
    parser = TitleParser()
    parser.feed(html)
    parser.close()
    return parser.title or "Title not found"


def fetch_title_sync(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        html = response.read().decode(charset, errors="replace")
    return extract_title(html)


def get_parser_context(session: Session) -> tuple[int, int]:
    user_id = session.execute(
        text(get_or_create_parser_user_sql()),
        {
            "email": settings.parser_user_email,
            "username": settings.parser_username,
            "hashed_password": "parser-service-user",
        },
    ).scalar_one()

    trip_id = session.execute(
        text(get_parser_trip_id_sql()),
        {
            "owner_id": user_id,
            "title": settings.parser_trip_title,
        },
    ).scalar_one_or_none()

    if trip_id is None:
        trip_id = session.execute(
            text(get_create_parser_trip_sql()),
            {
                "owner_id": user_id,
                "title": settings.parser_trip_title,
                "departure_city": "Internet",
                "destination_city": "Travel Buddy",
                "route_details": "Parsed web page titles saved by lab2/task2.",
            },
        ).scalar_one()

    return user_id, trip_id


def init_database() -> None:
    with get_session() as session:
        get_parser_context(session)
        session.commit()


def save_result(url: str, title: str, parser_type: str) -> None:
    created_at = datetime.now()

    with get_session() as session:
        user_id, trip_id = get_parser_context(session)

        session.execute(
            text(get_insert_message_sql()),
            {
                "trip_id": trip_id,
                "author_id": user_id,
                "content": f"[{parser_type}] {url} -> {title}",
                "created_at": created_at,
            },
        )

        session.commit()
