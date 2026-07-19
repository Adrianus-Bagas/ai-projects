"""
User Model.

Model ini merepresentasikan tabel `users` di PostgreSQL.

Tanggung jawab:
- Menyimpan informasi pengguna.
- Menjadi representasi ORM untuk tabel users.
"""

# Membuat UUID secara otomatis.
import uuid

# Python mengetahui bahwa id bertipe UUID.
from uuid import UUID

# SQLAlchemy Type untuk PostgreSQL.
from sqlalchemy import Uuid, String, DateTime, func

# ORM SQLAlchemy.
from sqlalchemy.orm import Mapped, mapped_column

# Base ORM kita.
from database.base import Base

from datetime import datetime

class User(Base):
    """
    Model ORM untuk tabel users.

    Semua object User akan dipetakan
    menjadi baris pada tabel users.
    """

    # Nama tabel di PostgreSQL.
    __tablename__ = "users"

    # Primary Key unik untuk setiap user.
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

    # Nama lengkap pengguna.
    # Wajib diisi dan dibatasi maksimal 255 karakter.
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
)
    
    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False,
)
    
    is_active: Mapped[bool] = mapped_column(
    default=True,
    nullable=False,
)