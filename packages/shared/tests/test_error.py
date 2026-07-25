from shared.responses import ErrorDetail, ErrorResponse


response = ErrorResponse(
    message="Invalid email or password",
    error=ErrorDetail(code="INVALID_CREDENTIALS"),
)

print(response.model_dump())