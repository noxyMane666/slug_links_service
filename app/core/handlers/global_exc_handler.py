from fastapi import Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.exceptions.domain_exceptions import (
    DomainException,
    LongUrlNotFoundException,
    SlugAlreadyExistsException
)

_DOMAIN_EXCEPTIONS_STATUS_CODES: dict[type, int] = {
    LongUrlNotFoundException: 404,
    SlugAlreadyExistsException: 409
}
_UNMAPPED_DOMAIN_EXCEPTION_STATUS_CODE: int = 500

def register_exception_handler(app: FastAPI) -> None:
    handler = GlobalExceptionHandler()
    app.add_exception_handler(HTTPException, handler.handle)
    app.add_exception_handler(RequestValidationError, handler.handle)
    app.add_exception_handler(DomainException, handler.handle)
    app.add_exception_handler(Exception, handler.handle)

class GlobalExceptionHandler:
    def __init__(self):
        pass

    @staticmethod
    def _generate_headers(request: Request, headers: dict[str, str] | None = None) -> dict[str, str]:
        headers = headers or {}
        request_id = getattr(request.state, 'request_id', None)
        if request_id:
            headers["x-request-id"] = request_id

        return headers

    def handle(self, request: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, DomainException):
            status_code = _DOMAIN_EXCEPTIONS_STATUS_CODES.get(type(exc), _UNMAPPED_DOMAIN_EXCEPTION_STATUS_CODE)
            return JSONResponse(
                status_code=status_code,
                content={"message": str(exc), "type": type(exc).__name__},
                headers=self._generate_headers(request)
            )
        elif isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={"message": exc.detail, "type": "HTTPException"},
                headers=self._generate_headers(request, exc.headers)
            )
        elif isinstance(exc, RequestValidationError):
            details = jsonable_encoder(exc.errors())
            return JSONResponse(
                status_code=422,
                content={"message": "ValidationError", "type": "RequestValidationError", "details": details},
                headers=self._generate_headers(request)
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error", "type": "InternalError"},
                headers=self._generate_headers(request)
            )