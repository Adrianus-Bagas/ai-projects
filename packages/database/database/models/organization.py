"""
Organization Model.

Model ini merepresentasikan tabel `organizations` di PostgreSQL.

Tanggung jawab:
- Menyimpan informasi organisasi.
- Menjadi representasi ORM untuk tabel organizations.
"""

# Membuat UUID secara otomatis.
import uuid

# Python mengetahui bahwa id bertipe UUID.
from uuid import UUID

# SQLAlchemy Type untuk PostgreSQL.
from sqlalchemy import Uuid, String

# ORM SQLAlchemy.
from sqlalchemy.orm import Mapped, mapped_column

# Base ORM kita.
from database.base import Base
from database.mixins import AuditTimestampMixin, VersionMixin

class Organization(
    VersionMixin,
    AuditTimestampMixin,
    Base,
):
    """
    Model ORM untuk tabel organizations.

    Semua object Organization akan dipetakan
    menjadi baris pada tabel organizations.
    """

    # Nama tabel di PostgreSQL.
    __tablename__ = "organizations"

    # Primary Key unik untuk setiap organization.
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

    # Nama organisasi.
    # Wajib diisi dan dibatasi maksimal 255 karakter.
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )