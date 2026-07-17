"""
Base Model untuk seluruh ORM SQLAlchemy.

Tanggung jawab:
- Menyediakan Base Class untuk semua model database.
- Menyimpan Metadata seluruh tabel aplikasi.

File ini tidak bertugas:
- Membuat Engine.
- Membuat Session.
- Menjalankan Query.
"""

# DeclarativeBase adalah class bawaan SQLAlchemy 2.0
# yang digunakan sebagai dasar (base class)
# untuk seluruh model ORM.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class seluruh model.

    Semua model ORM harus mewarisi class ini.

    Contoh:

        class User(Base):
            ...

        class Organization(Base):
            ...

    Dengan mewarisi Base,
    SQLAlchemy akan mengenali class tersebut
    sebagai model database.
    """

    # Untuk saat ini kita belum perlu menambahkan apa pun.
    # Namun di masa depan, kita bisa menambahkan:
    #
    # - created_at
    # - updated_at
    # - soft delete helper
    # - utility method
    #
    # yang otomatis dimiliki semua model.
    pass