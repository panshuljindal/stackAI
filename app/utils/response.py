from fastapi.responses import JSONResponse
from typing import Any

def sendResponse(status_code: int, message: str, body: Any = None) -> JSONResponse:

    return JSONResponse(
        status_code = status_code,
        content = {
            "status": "success" if 200 <= status_code < 300 else "error",
            "message": message,
            "body": body
        }
    )