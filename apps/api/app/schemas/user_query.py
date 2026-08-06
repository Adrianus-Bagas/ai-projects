from pydantic import BaseModel, Field
from enum import StrEnum

from database.models.enums import UserRole
from shared.schemas.sorting import SortOrder

class UserFilterParams(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None
    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

class UserSortField(StrEnum):
    CREATED_AT = "created_at"
    NAME = "name"
    EMAIL = "email"
    ROLE = "role"


class UserSortingParams(BaseModel):
    sort_by: UserSortField = UserSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC