"""
Organization Membership Model.

Model ini merepresentasikan tabel `organization_memberships` di PostgreSQL.

Tanggung jawab:
- Menyimpan informasi relasi organizations dan users.
- Menjadi representasi ORM untuk tabel organization_memberships.
"""

# Membuat UUID secara otomatis.
import uuid

# Python mengetahui bahwa id bertipe UUID.
from uuid import UUID

# SQLAlchemy Type untuk PostgreSQL.
from sqlalchemy import Uuid, Enum, UniqueConstraint, ForeignKey

# ORM SQLAlchemy.
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base ORM kita.
from database.base import Base
from database.mixins import AuditTimestampMixin, VersionMixin

from database.models.enums import OrganizationRole

class OrganizationMembership(
    VersionMixin,
    AuditTimestampMixin,
    Base,
):
    """
    Model ORM untuk tabel organization_memberships.

    Semua object OrganizationMembership akan dipetakan
    menjadi baris pada tabel organization_memberships.
    """

    # Nama tabel di PostgreSQL.
    __tablename__ = "organization_memberships"
    
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_organization_memberships_organization_user",
        ),
    )

    # Primary Key unik untuk setiap organization membership.
    #
    # UUID dipilih karena:
    # - Sulit ditebak.
    # - Aman untuk API.
    # - Cocok untuk distributed system.
    id: Mapped[UUID] = mapped_column(

        # PostgreSQL UUID type.
        Uuid,

        # Menjadi Primary Key.
        primary_key=True,

        # Dibuat otomatis setiap object baru.
        default=uuid.uuid4,
    )
    
    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    
    organization_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    
    role: Mapped[OrganizationRole] = mapped_column(
        Enum(
            OrganizationRole,
            name="organization_role",
            values_callable=lambda enum_class: [
                role.value for role in enum_class
            ],
        ),
        default=OrganizationRole.MEMBER,
        nullable=False,
    ) 
    
    user: Mapped["User"] = relationship(
        back_populates="organization_memberships",
    )
    
    organization: Mapped["Organization"] = relationship(
        back_populates="memberships",
    )