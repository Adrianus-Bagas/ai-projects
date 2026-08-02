import uuid
from typing import Any
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.mixins.audit_timestamp import AuditTimestampMixin
from database.models.enums import AuditAction


class AuditLog(AuditTimestampMixin, Base):
    __tablename__ = "audit_logs"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    actor_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        Enum(
            AuditAction,
            name="audit_action",
            values_callable=lambda enum_class: [
                action.value for action in enum_class
            ],
        ),
        nullable=False,
        index=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )

    event_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )

    changes: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )