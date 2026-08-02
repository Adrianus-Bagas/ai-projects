from pydantic import BaseModel, Field

from database.models.enums import UserRole


class UserFilterParams(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None
    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )