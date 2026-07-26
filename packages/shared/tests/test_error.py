from shared.responses import ErrorDetail, ErrorResponse
from shared.errors import (
    INTERNAL_SERVER_ERROR_MESSAGE,
    SharedErrorCode,
)
from shared.errors.mappers import map_http_error_code

response = ErrorResponse(
    message="Invalid email or password",
    error=ErrorDetail(code="INVALID_CREDENTIALS"),
)

print(response.model_dump())

print(map_http_error_code(404))
print(map_http_error_code(405))
print(map_http_error_code(403))

print(SharedErrorCode.INTERNAL_SERVER_ERROR)
print(INTERNAL_SERVER_ERROR_MESSAGE)