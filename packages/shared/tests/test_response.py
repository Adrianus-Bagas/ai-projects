from shared.responses import ApiResponse


response = ApiResponse[str](
    success=True,
    message="Test successful",
    data="Hello",
)

print(response.model_dump())