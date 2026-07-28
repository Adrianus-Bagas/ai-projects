from uuid import UUID

from pydantic import BaseModel, ConfigDict

from database.models.enums import UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    email: str
    role: UserRole
    is_active: bool