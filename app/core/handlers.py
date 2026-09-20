"""Central exception handlers: every error class returns the section 6 envelope (FR-224)."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError, ErrorDetail, RateLimited
from app.core.responses import GENERIC_500, error_response

_HTTP_CODES: dict[int, tuple[str, str]] = {
    400: ("MALFORMED_REQUEST", "The request could not be understood."),
    401: ("UNAUTHENTICATED", "The access token is missing, invalid or expired."),
    403: ("FORBIDDEN", "You are not allowed to do this."),
    404: ("NOT_FOUND", "The resource or route was not found."),
    405: ("METHOD_NOT_ALLOWED", "This method is not supported on this path."),
    413: ("PAYLOAD_TOO_LARGE", "The request body is too large."),
    415: ("UNSUPPORTED_MEDIA_TYPE", "The content type must be application/json."),
}


async def handle_app_error(_: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, AppError)  # noqa: S101 - narrows the type for mypy
    headers = {"Retry-After": str(error.retry_after)} if isinstance(error, RateLimited) else None
    return error_response(error.status_code, error.code, error.message, error.details, headers)


def _field(location: tuple[int | str, ...]) -> str:
    parts = [str(part) for part in location if part not in ("body", "query", "path")]
    return ".".join(parts) or "body"


async def handle_validation_error(_: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, RequestValidationError)  # noqa: S101
    problems = error.errors()
    if any(item["type"] == "json_invalid" for item in problems):
        return error_response(400, "MALFORMED_REQUEST", "The request body is not valid JSON.")
    details = [
        ErrorDetail(_field(tuple(item["loc"])), str(item["msg"]).removeprefix("Value error, "))
        for item in problems
    ]
    return error_response(422, "VALIDATION_ERROR", "One or more fields are invalid.", details)


async def handle_http_exception(_: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, StarletteHTTPException)  # noqa: S101
    code, message = _HTTP_CODES.get(error.status_code, ("INTERNAL_ERROR", GENERIC_500))
    headers = (
        {"Allow": error.headers["Allow"]} if error.headers and "Allow" in error.headers else None
    )
    return error_response(error.status_code, code, message, None, headers)


async def handle_unexpected(_: Request, __: Exception) -> JSONResponse:
    return error_response(500, "INTERNAL_ERROR", GENERIC_500)


def register_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, handle_app_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(StarletteHTTPException, handle_http_exception)
    app.add_exception_handler(Exception, handle_unexpected)
