"""
Database Engine.

Tanggung jawab:
- Membuat satu AsyncEngine.
- Mengelola Connection Pool.
- Menjadi pintu masuk komunikasi dengan PostgreSQL.

File ini TIDAK bertanggung jawab untuk:
- Membuat Session.
- Menjalankan Query.
- Mendefinisikan Model.
"""

# Fungsi factory dari SQLAlchemy untuk membuat AsyncEngine.
# Kita menggunakan factory karena proses pembuatan Engine cukup kompleks.
from sqlalchemy.ext.asyncio import create_async_engine

# Mengambil konfigurasi database yang sudah kita buat sebelumnya.
from database.config import settings


# Membuat satu AsyncEngine.
#
# Engine ini akan hidup selama aplikasi berjalan.
# Seluruh request akan menggunakan Engine yang sama.
engine = create_async_engine(

    # URL koneksi menuju PostgreSQL.
    url=settings.database_url,

    # Menampilkan SQL Query ke terminal jika echo=True.
    # Sangat membantu saat debugging.
    echo=settings.echo,

    # Jumlah koneksi minimum yang dipertahankan di pool.
    pool_size=settings.pool_size,

    # Jumlah koneksi tambahan jika pool utama penuh.
    max_overflow=settings.max_overflow,

    # Mengecek apakah koneksi masih hidup sebelum digunakan.
    # Ini membantu menghindari penggunaan koneksi yang sudah terputus.
    pool_pre_ping=True,
)