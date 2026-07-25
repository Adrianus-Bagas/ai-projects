from shared.responses import ErrorDetail, ErrorResponse, FieldError


response = ErrorResponse(
    message="Request validation failed",
    error=ErrorDetail(
        code="VALIDATION_ERROR",
        details=[
            FieldError(
                field="email",
                message="Invalid email address",
                type="value_error",
            )
        ],
    ),
)

print(response.model_dump(exclude_none=True))