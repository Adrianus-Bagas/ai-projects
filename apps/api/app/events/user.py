from dataclasses import dataclass
from uuid import UUID

from app.events.base import DomainEvent
from database.models.enums import UserRole


@dataclass(frozen=True, kw_only=True)
class UserRoleChanged(DomainEvent):
    user_id: UUID
    actor_id: UUID
    old_role: UserRole
    new_role: UserRole