"""
Database configuration.

Tanggung jawab:
- Membaca konfigurasi database dari environment variable.
- Melakukan validasi konfigurasi menggunakan Pydantic.
- Menyediakan object settings yang dapat digunakan oleh seluruh aplikasi.

File ini TIDAK bertanggung jawab untuk:
- Membuat database engine.
- Membuat session.
- Menjalankan query SQL.
"""

# BaseSettings digunakan untuk membaca environment variable secara otomatis.
from pydantic_settings import BaseSettings

# SettingsConfigDict digunakan untuk mengatur bagaimana BaseSettings bekerja,
# misalnya lokasi file .env dan encoding yang digunakan.
from pydantic_settings import SettingsConfigDict


# Class ini menyimpan seluruh konfigurasi database.
#
# Kenapa menggunakan class?
#
# Karena:
# - lebih mudah divalidasi
# - memiliki autocomplete
# - type-safe
# - mudah digunakan kembali oleh package lain
class DatabaseSettings(BaseSettings):

    # URL koneksi menuju PostgreSQL.
    #
    # Nilainya akan otomatis diambil dari environment variable:
    #
    # DATABASE_URL=postgresql+asyncpg://...
    database_url: str

    # Jumlah minimum koneksi yang akan disimpan di Connection Pool.
    #
    # Nilai default:
    # 5
    #
    # Artinya SQLAlchemy akan mencoba mempertahankan 5 koneksi aktif.
    pool_size: int = 5

    # Jumlah koneksi tambahan jika pool utama penuh.
    #
    # Misalnya:
    #
    # pool_size = 5
    # max_overflow = 10
    #
    # Maka maksimal koneksi adalah 15.
    max_overflow: int = 10

    # Menentukan apakah SQLAlchemy akan menampilkan seluruh SQL Query
    # ke terminal.
    #
    # True:
    # SELECT ...
    #
    # False:
    # tidak menampilkan query.
    #
    # Saat development biasanya True.
    # Saat production biasanya False.
    echo: bool = False

    # Konfigurasi BaseSettings.
    #
    # env_file
    # --------
    # Memberitahu Pydantic untuk membaca file .env.
    #
    # extra="ignore"
    # --------------
    # Mengabaikan environment variable lain yang tidak digunakan.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Membuat satu instance settings.
#
# Mengapa dibuat di sini?
#
# Karena seluruh aplikasi akan menggunakan object yang sama.
#
# Jadi nanti cukup:
#
# from database.config import settings
#
settings = DatabaseSettings()