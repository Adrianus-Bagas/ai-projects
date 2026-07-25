from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    
class FieldError(BaseModel):
    field: str
    message: str
    type: str

class ErrorDetail(BaseModel):
    code: str
    details: list[FieldError] | None = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: ErrorDetail