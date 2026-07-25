from fastapi import Request
from fastapi.responses import JSONResponse

from shared.errors.exceptions import AppException
from fastapi.exceptions import RequestValidationError

from shared.responses import (
    ErrorDetail,
    ErrorResponse,
    FieldError,
)

from http import HTTPStatus

from shared.errors.constants import (
    SharedErrorCode,
    VALIDATION_ERROR_MESSAGE,
)


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