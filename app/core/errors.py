from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Any

class AppException(Exception):
    def __init__(self, code: str, message: str, details: str | None = None, http_status: int = 400):
        self.code = code
        self.message = message
        self.details = details
        self.http_status = http_status

def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.http_status,
        content={
            "status": "error",
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )

def validation_exception_handler(request: Request, exc: ValidationError):
    # Transform pydantic validation into required JSON error format
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error": {
                "code": "INVALID_FORMAT",
                "message": "Formato de mensaje inválido",
                "details": str(exc.errors()),
            },
        },
    )

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail if isinstance(exc.detail, str) else "HTTP error",
                "details": None,
            },
        },
    )
