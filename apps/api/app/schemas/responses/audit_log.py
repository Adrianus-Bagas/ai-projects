from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from database.models.enums import AuditAction


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    actor_id: UUID | None
    action: AuditAction
    entity_type: str
    entity_id: UUID
    event_name: str | None
    changes: dict[str, Any] | None
    created_at: datetime