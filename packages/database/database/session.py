"""
Database Session.

Tanggung jawab:
- Membuat Session untuk setiap request.
- Memastikan Session selalu ditutup setelah selesai digunakan.

File ini tidak bertugas:
- Membuat Engine.
- Menjalankan Query.
- Mendefinisikan Model.
"""

# Import generator typing.
# AsyncGenerator memberi tahu bahwa fungsi ini akan menggunakan `yield`.
from typing import AsyncGenerator

# AsyncSession adalah objek yang akan kita gunakan
# untuk menjalankan query ke database.
#
# async_sessionmaker adalah factory untuk membuat Session baru.
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

# Menggunakan Engine yang sudah kita buat sebelumnya.
from database.engine import engine


# Factory pembuat Session.
#
# Bayangkan seperti cetakan.
# Setiap kali dipanggil, factory ini akan membuat
# Session baru yang terhubung ke Engine yang sama.
SessionLocal = async_sessionmaker(

    # Engine yang akan digunakan.
    bind=engine,

    # Setelah commit, object tetap bisa digunakan.
    expire_on_commit=False,

    # Semua Session yang dibuat akan berupa AsyncSession.
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency FastAPI.

    Setiap request akan mendapatkan Session baru.

    Setelah request selesai,
    Session akan otomatis ditutup.
    """

    # Membuat Session baru.
    async with SessionLocal() as session:

        try:
            # Mengirim Session ke endpoint.
            yield session

        finally:
            # Session selalu ditutup.
            #
            # Walaupun terjadi Exception,
            # bagian finally tetap dijalankan.
            await session.close()