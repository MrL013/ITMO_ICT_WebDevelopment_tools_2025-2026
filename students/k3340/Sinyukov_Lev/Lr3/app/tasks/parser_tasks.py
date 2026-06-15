from __future__ import annotations

from app.celery_app import celery_app
from app.services.parser_engine import parse_and_store_url


@celery_app.task(name="app.tasks.parse_url_task")
def parse_url_task(url: str) -> dict[str, object]:
    return parse_and_store_url(url, "celery")
