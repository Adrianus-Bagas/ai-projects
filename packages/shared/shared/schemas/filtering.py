from pydantic import BaseModel

from database.models.enums import UserRole


class UserFilterParams(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None