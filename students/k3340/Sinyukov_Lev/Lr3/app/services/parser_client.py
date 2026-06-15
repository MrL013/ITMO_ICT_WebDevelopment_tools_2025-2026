from __future__ import annotations

import requests
from fastapi import HTTPException, status

from app.core.config import settings


def request_parser(url: str) -> dict[str, object]:
    parser_url = f"{settings.parser_service_url.rstrip('/')}" + "/parse"

    try:
        response = requests.post(
            parser_url,
            json={"url": url},
            timeout=settings.parser_request_timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Parser service request failed: {error}",
        ) from error
