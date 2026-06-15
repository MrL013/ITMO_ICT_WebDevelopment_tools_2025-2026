from fastapi import APIRouter, status
from celery.result import AsyncResult

from app.celery_app import celery_app
from app.schemas.parser import ParseRequest, ParseResponse, ParseTaskQueuedResponse, ParseTaskStatusResponse
from app.services.parser_client import request_parser
from app.tasks.parser_tasks import parse_url_task

router = APIRouter(prefix="/parser", tags=["parser"])


@router.post("/parse", response_model=ParseResponse)
def parse_url_via_http(data: ParseRequest) -> ParseResponse:
    result = request_parser(str(data.url))
    return ParseResponse.model_validate(result)


@router.post("/parse-async", response_model=ParseTaskQueuedResponse, status_code=status.HTTP_202_ACCEPTED)
def parse_url_async(data: ParseRequest) -> ParseTaskQueuedResponse:
    task = parse_url_task.delay(str(data.url))
    return ParseTaskQueuedResponse(
        task_id=task.id,
        status="PENDING",
        message="Parsing task has been queued",
    )


@router.get("/tasks/{task_id}", response_model=ParseTaskStatusResponse)
def get_task_status(task_id: str) -> ParseTaskStatusResponse:
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return ParseTaskStatusResponse(task_id=task_id, status="PENDING")

    if task_result.state == "FAILURE":
        return ParseTaskStatusResponse(task_id=task_id, status="FAILURE", error=str(task_result.info))

    if task_result.state == "SUCCESS":
        return ParseTaskStatusResponse(
            task_id=task_id,
            status="SUCCESS",
            result=ParseResponse.model_validate(task_result.result),
        )

    return ParseTaskStatusResponse(task_id=task_id, status=task_result.state)
