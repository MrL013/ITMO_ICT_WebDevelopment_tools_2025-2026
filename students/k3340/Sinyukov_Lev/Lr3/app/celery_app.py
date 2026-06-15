from __future__ import annotations

from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "travel_buddy_lab3",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.parser_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)
