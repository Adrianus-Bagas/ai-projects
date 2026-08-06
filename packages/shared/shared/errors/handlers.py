from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.orm.exc import StaleDataError

from shared.errors.mappers import map_http_error_code

from shared.errors.exceptions import AppException
from fastapi.exceptions import RequestValidationError

from shared.responses import (
    ErrorDetail,
    ErrorResponse,
    FieldError,
)

from http import HTTPStatus
import logging

from shared.errors.constants import (
    SharedErrorCode,
    VALIDATION_ERROR_MESSAGE,
    INTERNAL_SERVER_ERROR_MESSAGE,
    RESOURCE_CONFLICT_MESSAGE
)

logger = logging.getLogger(__name__)

async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    response = ErrorResponse(
        message=exc.message,
        error=ErrorDetail(code=exc.error_code),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(exclude_none=True),
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    field_errors: list[FieldError] = []

    for error in exc.errors():
        location = error["loc"]
        field = ".".join(str(part) for part in location if part != "body")

        field_errors.append(
            FieldError(
                field=field,
                message=error["msg"],
                type=error["type"],
            )
        )

    response = ErrorResponse(
        message=VALIDATION_ERROR_MESSAGE,
        error=ErrorDetail(
            code=SharedErrorCode.VALIDATION_ERROR,
            details=field_errors,
        ),
    )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=response.model_dump(exclude_none=True),
    )

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    message = (
        exc.detail
        if isinstance(exc.detail, str)
        else HTTPStatus(exc.status_code).phrase
    )

    response = ErrorResponse(
        message=message,
        error=ErrorDetail(
            code=map_http_error_code(exc.status_code),
        ),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(exclude_none=True),
        headers=exc.headers,
    )

async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unexpected error while processing %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )

    response = ErrorResponse(
        message=INTERNAL_SERVER_ERROR_MESSAGE,
        error=ErrorDetail(
            code=SharedErrorCode.INTERNAL_SERVER_ERROR,
        ),
    )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=response.model_dump(exclude_none=True),
    )

async def stale_data_exception_handler(
    request: Request,
    exc: StaleDataError,
) -> JSONResponse:
    logger.warning(
        "Optimistic locking conflict while processing %s %s",
        request.method,
        request.url.path,
    )

    response = ErrorResponse(
        message=RESOURCE_CONFLICT_MESSAGE,
        error=ErrorDetail(
            code=SharedErrorCode.RESOURCE_CONFLICT,
        ),
    )

    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content=response.model_dump(exclude_none=True),
    )