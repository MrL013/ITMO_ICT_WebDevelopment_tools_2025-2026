from fastapi import FastAPI, HTTPException
import requests

from app.core.config import settings
from app.schemas.parser import ParseRequest, ParseResponse
from app.services.parser_engine import parse_and_store_url

app = FastAPI(title=settings.parser_service_name)


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse", response_model=ParseResponse)
def parse_endpoint(data: ParseRequest) -> ParseResponse:
    try:
        result = parse_and_store_url(str(data.url), "http-parser")
        return ParseResponse.model_validate(result)
    except requests.RequestException as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
