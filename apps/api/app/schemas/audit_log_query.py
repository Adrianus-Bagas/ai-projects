from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from database.models.enums import AuditAction
from shared.schemas.sorting import SortOrder


class AuditLogSortField(StrEnum):
    CREATED_AT = "created_at"
    ACTION = "action"
    ENTITY_TYPE = "entity_type"
    EVENT_NAME = "event_name"


class AuditLogSortingParams(BaseModel):
    sort_by: AuditLogSortField = AuditLogSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC


class AuditLogFilterParams(BaseModel):
    action: AuditAction | None = None
    entity_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    actor_id: UUID | None = None
    entity_id: UUID | None = None
    event_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )