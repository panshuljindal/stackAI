from fastapi.responses import JSONResponse
from typing import Any, Optional
from pydantic.json import pydantic_encoder
import json

def sendResponse(
    status_code: int,
    message: str,
    body: Optional[Any] = None
) -> JSONResponse:
    content = {
        "status_code": status_code,
        "message": message,
        "body": body,
    }

    return JSONResponse(
        content=json.loads(json.dumps(content, default=pydantic_encoder)),
        status_code=status_code
    )
