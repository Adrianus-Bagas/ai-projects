# Project Architecture

Dokumen ini menjelaskan prinsip arsitektur utama yang digunakan dalam project.

Tujuannya adalah menjaga struktur project tetap konsisten ketika jumlah fitur, model, service, repository, dan kontributor bertambah.

---

## 1. Dependency Direction

Dependency utama aplikasi bergerak dalam satu arah:

```text
HTTP Endpoint
      ↓
Application Service
      ↓
Repository
      ↓
Database Model
```

Layer yang lebih rendah tidak boleh bergantung pada layer yang lebih tinggi.

Arah dependency yang diperbolehkan:

```text
Endpoint → Service
Service → Repository
Repository → Database Model
Application → Shared Package
Application → Database Package
```

Arah dependency yang tidak diperbolehkan:

```text
Repository → FastAPI
Repository → Service
Database Model → Repository
Database Package → Application
Shared Package → Application
```

Tujuan aturan ini adalah mencegah circular dependency, menjaga batas antarlayer, dan membuat setiap komponen lebih mudah diuji serta digunakan ulang.

---

## 2. HTTP Endpoint

Endpoint merupakan pintu masuk HTTP aplikasi.

Endpoint bertanggung jawab terhadap:

- menerima request HTTP,
- menjalankan dependency authentication,
- menjalankan dependency authorization,
- menerima request body dan query parameter,
- memanggil application service,
- membentuk response API,
- menentukan response model.

Endpoint tidak boleh:

- menjalankan query database secara langsung,
- membuat database session,
- membuat repository secara langsung,
- mengelola commit atau rollback,
- menyimpan business rule,
- menangani detail persistence.

Contoh:

```python
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> ApiResponse[PaginatedResponse[UserResponse]]:
    users = await user_service.get_all_users(...)

    return ApiResponse(
        success=True,
        message="Users retrieved successfully",
        data=users,
    )
```

---

## 3. Application Service

Application service mengatur proses bisnis aplikasi.

Service bertanggung jawab terhadap:

- business rule,
- validasi proses bisnis,
- orchestration repository,
- transaction boundary,
- application exception,
- transformasi model menjadi hasil aplikasi,
- koordinasi beberapa operasi dalam satu use case.

Service tidak boleh:

- bergantung pada FastAPI,
- menerima `Request` atau `Response`,
- menggunakan `Depends`,
- membuat database session sendiri,
- membuat repository sendiri,
- menulis query SQLAlchemy secara langsung,
- menentukan response HTTP.

Contoh:

```python
async with self.transaction_manager:
    user.role = role

    updated_user = await self.user_repository.save(
        entity=user,
    )
```

Service menentukan kapan sebuah proses bisnis dianggap berhasil dan layak di-commit.

---

## 4. Repository

Repository menangani komunikasi antara aplikasi dan database.

Repository bertanggung jawab terhadap:

- query database,
- mengambil ORM model,
- menyimpan perubahan ORM model,
- filtering,
- sorting,
- pagination,
- search,
- persistence-specific behavior,
- soft-delete criteria,
- query khusus suatu entity.

Repository tidak boleh:

- mengembalikan HTTP response,
- menggunakan `HTTPException`,
- menentukan HTTP status code,
- mengetahui endpoint,
- mengetahui `Request`,
- menyimpan business rule,
- membuat database session sendiri.

Repository boleh mengeluarkan exception persistence seperti:

```text
StaleDataError
IntegrityError
```

Exception persistence dapat diterjemahkan menjadi application error atau HTTP response oleh layer yang lebih tinggi.

---

## 5. Base Repository

`BaseRepository` hanya berisi operasi yang benar-benar dapat digunakan oleh banyak repository.

Contoh tanggung jawabnya:

```text
get_by_id
get_by_id_including_deleted
get_all
add
save
delete
refresh
commit
rollback
```

Query yang hanya relevan terhadap entity tertentu harus tetap berada di repository spesifik.

Contoh:

```text
UserRepository.get_by_email
UserRepository.get_paginated
UserRepository._build_filters
```

Abstraksi generic tidak boleh memaksakan konsep khusus suatu entity ke semua repository.

---

## 6. Database Package

Package `database` bertanggung jawab terhadap:

- SQLAlchemy engine,
- async session factory,
- declarative base,
- ORM model,
- ORM mixin,
- database metadata.

Package database tidak boleh bergantung pada:

```text
app.api
app.services
app.repositories
FastAPI
```

Arah dependency yang benar:

```text
Application → Database Package
```

Bukan:

```text
Database Package → Application
```

Struktur utama package database:

```text
packages/database/database/
├── base.py
├── engine.py
├── session.py
├── mixins/
└── models/
```

---

## 7. ORM Mixins

Mixin digunakan untuk memberikan kemampuan ORM yang reusable tanpa memasukkan semua perilaku ke declarative base.

Mixin yang tersedia:

```text
AuditTimestampMixin
SoftDeleteMixin
VersionMixin
```

### AuditTimestampMixin

Menyediakan:

```text
created_at
updated_at
```

### SoftDeleteMixin

Menyediakan:

```text
deleted_at
```

### VersionMixin

Menyediakan:

```text
version
```

Tidak semua model wajib memakai seluruh mixin.

Contohnya, `AuditLog` bersifat append-only sehingga tidak menggunakan `SoftDeleteMixin` atau `VersionMixin`.

---

## 8. Database Session

Setiap request menggunakan satu instance `AsyncSession`.

Session dibuat oleh:

```python
get_db()
```

Repository dan `TransactionManager` dalam request yang sama harus menerima instance session yang sama.

Dependency graph:

```text
get_db()
   │
   ├── UserRepository
   │
   └── TransactionManager
            │
            ▼
        UserService
```

Repository, service, dan transaction manager tidak boleh membuat `SessionLocal()` sendiri selama menangani request aplikasi.

Session baru hanya boleh dibuat secara eksplisit untuk kebutuhan seperti:

- maintenance script,
- migration script,
- background worker,
- development utility,
- integration test.

---

## 9. Transaction Management

Transaction boundary dikelola oleh application service menggunakan `TransactionManager`.

Contoh:

```python
async with self.transaction_manager:
    user.role = role

    updated_user = await self.user_repository.save(
        entity=user,
    )
```

Perilakunya:

```text
Success
→ commit

Exception dalam blok
→ rollback
→ exception diteruskan

Exception saat commit
→ rollback
→ exception diteruskan
```

Repository tidak menentukan kapan keseluruhan proses bisnis harus di-commit.

Method seperti `save()` hanya melakukan persistence preparation seperti:

```text
add
flush
refresh
```

Commit dilakukan setelah seluruh proses bisnis selesai tanpa error.

---

## 10. Soft Delete

Business entity yang mendukung soft delete menggunakan:

```python
deleted_at
```

Data aktif:

```text
deleted_at IS NULL
```

Data yang sudah dihapus:

```text
deleted_at IS NOT NULL
```

Operasi delete normal tidak menjalankan hard delete.

Secara konsep:

```sql
UPDATE users
SET deleted_at = NOW()
WHERE id = ...;
```

Query normal harus hanya mengembalikan data aktif.

Akses terhadap data yang sudah dihapus harus dilakukan secara eksplisit, misalnya:

```python
get_by_id_including_deleted(...)
```

Prinsip yang digunakan:

```text
Safe by default
Explicit when exceptional
```

Audit log tidak menggunakan soft delete karena catatan audit harus tetap utuh.

---

## 11. Optimistic Locking

Entity yang dapat diperbarui menggunakan kolom:

```python
version
```

SQLAlchemy menggunakan konfigurasi:

```python
__mapper_args__ = {
    "version_id_col": version,
}
```

Saat entity diperbarui, SQLAlchemy menjalankan query yang secara konsep berbentuk:

```sql
UPDATE users
SET
    role = 'admin',
    version = 2
WHERE
    id = ...
    AND version = 1;
```

Jika versi database sudah berubah, tidak ada row yang berhasil diperbarui dan SQLAlchemy menghasilkan:

```text
StaleDataError
```

Alurnya:

```text
StaleDataError
→ TransactionManager rollback
→ Global exception handler
→ HTTP 409 Conflict
```

Optimistic locking digunakan untuk mencegah lost update ketika beberapa transaksi memperbarui entity yang sama.

---

## 12. Audit Log

Audit log mencatat perubahan state entity.

Field utama audit log:

```text
id
actor_id
action
entity_type
entity_id
event_name
changes
created_at
updated_at
```

Audit log bersifat append-only.

Operasi yang diperbolehkan:

```text
create
read
```

Operasi yang tidak diperbolehkan:

```text
update
delete
soft delete
```

Audit log harus tetap utuh agar riwayat aktivitas aplikasi dapat dipercaya.

`actor_id` menggunakan foreign key ke `users.id` dan dapat bernilai `NULL` untuk perubahan yang dilakukan oleh sistem.

`entity_id` tidak menggunakan foreign key karena audit log dapat menunjuk berbagai jenis entity.

Contoh nilai `changes`:

```json
{
  "role": {
    "old": "user",
    "new": "admin"
  }
}
```

Audit log fokus pada perubahan state entity. Kejadian aplikasi yang tidak selalu mengubah entity akan ditangani oleh application event system.

---

## 13. Shared Package

Package `shared` hanya berisi konsep yang benar-benar reusable lintas aplikasi, fitur, atau resource.

Contoh yang sesuai:

```text
ApiResponse
ErrorResponse
ErrorDetail
AppException
PaginationParams
PaginationMeta
PaginatedResponse
SortOrder
```

Konsep spesifik domain tidak boleh berada di `shared`.

Contoh yang tidak sesuai:

```text
UserFilterParams
UserSortField
UserSortingParams
```

Schema khusus user harus berada di application schema:

```text
apps/api/app/schemas/
```

Package `shared` tidak boleh bergantung pada application package.

---

## 14. Application Schemas

Schema yang spesifik terhadap request, response, atau query suatu fitur berada di:

```text
apps/api/app/schemas/
```

Contoh:

```text
auth.py
user_query.py
responses/
```

Schema aplikasi boleh bergantung pada:

```text
database model enums
shared generic schemas
```

Contoh:

```python
from database.models.enums import UserRole
from shared.schemas.sorting import SortOrder
```

Schema aplikasi tidak boleh menjalankan query atau menyimpan business logic.

---

## 15. Dependency Injection

Pembuatan object dilakukan pada dependency layer.

Contoh composition flow:

```text
AsyncSession
→ UserRepository
→ TransactionManager
→ UserService
→ Endpoint
```

Contoh struktur:

```text
app/dependencies/
├── current_user.py
├── repositories.py
├── require_roles.py
├── transaction.py
└── services/
```

Service dan repository tidak boleh membuat dependency sendiri.

Constructor injection digunakan agar dependency:

- eksplisit,
- mudah diuji,
- mudah diganti,
- tidak terikat langsung pada framework,
- mudah disusun pada composition layer.

Provider yang hanya membuat object dan tidak menjalankan operasi asynchronous sebaiknya menggunakan fungsi biasa:

```python
def get_user_repository(...) -> UserRepository:
    ...
```

---

## 16. Authentication and Authorization

Authentication menentukan siapa user yang sedang menjalankan request.

Authorization menentukan apakah user tersebut memiliki izin menjalankan operasi.

Dependency authentication dan authorization berada di endpoint layer, misalnya:

```python
current_user: User = Depends(get_current_user)
```

atau:

```python
_: User = Depends(
    require_roles(UserRole.ADMIN)
)
```

Business rule tambahan tetap dapat berada di service.

Contoh:

```text
Admin tidak boleh mengubah role miliknya sendiri
```

Rule tersebut merupakan proses bisnis, sehingga berada di `UserService`, bukan hanya di endpoint.

---

## 17. Error Handling

Application error menggunakan:

```python
AppException
```

Global exception handler mengubah exception menjadi response API yang konsisten.

Handler yang tersedia:

```text
AppException
RequestValidationError
HTTPException
StaleDataError
Unexpected Exception
```

Exception umum yang tidak dikenali menghasilkan:

```http
500 Internal Server Error
```

Detail exception internal hanya ditulis ke log dan tidak dikirim kepada client.

Contoh optimistic locking conflict:

```http
409 Conflict
```

```json
{
  "success": false,
  "message": "The resource was modified by another request. Please refresh the data and try again.",
  "error": {
    "code": "RESOURCE_CONFLICT"
  }
}
```

Repository tidak boleh menerjemahkan exception menjadi response HTTP.

---

## 18. Response Format

Response API menggunakan struktur yang konsisten.

Contoh response berhasil:

```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": {}
}
```

Contoh response gagal:

```json
{
  "success": false,
  "message": "Request validation failed",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": []
  }
}
```

Model response generic berada di package `shared`.

Endpoint tetap bertanggung jawab menentukan response model yang digunakan oleh suatu route.

---

## 19. Pagination, Sorting, Filtering, and Search

Endpoint list dapat mendukung:

```text
pagination
sorting
filtering
search
```

Pagination menggunakan parameter:

```text
page
page_size
```

Sorting menggunakan:

```text
sort_by
sort_order
```

Filtering dan search dibuat spesifik terhadap resource.

Query `COUNT(*)` dan query pengambilan data harus menerapkan kondisi filter serta search yang sama agar metadata pagination tetap akurat.

Sorting pagination harus deterministik.

Contoh:

```sql
ORDER BY name ASC, id ASC
```

Kolom `id` digunakan sebagai tie-breaker ketika nilai sorting utama sama.

Field sorting harus menggunakan whitelist eksplisit dan tidak menerima nama kolom database secara bebas.

---

## 20. Logging

Logging configuration berada di:

```text
app/core/logging.py
```

Exception yang tidak terduga dicatat menggunakan traceback.

Kondisi bisnis yang diperkirakan, seperti optimistic locking conflict, dapat dicatat sebagai warning tanpa dianggap sebagai internal application failure.

Log tidak boleh mengungkapkan informasi sensitif seperti:

```text
password
password hash
access token
secret key
authorization header
```

Response error internal tidak boleh menampilkan traceback kepada client.

---

## 21. Abstraction Rule

Abstraksi baru tidak dibuat berdasarkan prediksi semata.

Urutan yang digunakan:

```text
Implementasi konkret
→ pola berulang terlihat
→ masalah dipahami
→ abstraksi dibuat
```

Contoh abstraksi yang lahir dari kebutuhan nyata:

```text
BaseRepository
TransactionManager
AuditTimestampMixin
SoftDeleteMixin
VersionMixin
```

Hindari membuat komponen berikut sebelum ada kebutuhan dan pola berulang yang jelas:

```text
BaseService
GenericService
GenericQueryBuilder
GlobalUtilityClass
```

Abstraksi harus mengurangi duplikasi dan kompleksitas, bukan hanya memindahkan kompleksitas ke tempat lain.

---

## 22. Folder Placement Rules

Gunakan aturan berikut ketika menentukan lokasi file baru.

```text
HTTP route
→ app/api

Business process
→ app/services

Database query
→ app/repositories

Application request/response schema
→ app/schemas

Object composition
→ app/dependencies

Application infrastructure
→ app/core

ORM model and mixin
→ packages/database

Generic reusable contract
→ packages/shared
```

Folder generik seperti:

```text
utils
helpers
common
misc
```

sebaiknya dihindari kecuali tanggung jawab isinya benar-benar jelas.

---

## 23. Current Backend Structure

Struktur utama aplikasi API:

```text
apps/api/app/
├── api/
├── core/
├── dependencies/
├── repositories/
├── schemas/
└── services/
```

Package database:

```text
packages/database/database/
├── base.py
├── engine.py
├── session.py
├── mixins/
└── models/
```

Package shared:

```text
packages/shared/shared/
├── errors/
├── responses/
└── schemas/
```

Setiap file dan folder baru harus mengikuti batas tanggung jawab yang dijelaskan dalam dokumen ini.

---

## 24. Architecture Evolution

Dokumen ini mencerminkan arsitektur project saat ini.

Arsitektur dapat berkembang ketika muncul kebutuhan baru, tetapi perubahan harus:

1. memiliki masalah nyata yang ingin diselesaikan,
2. menjaga arah dependency,
3. menghindari coupling antarlayer,
4. mempertahankan compatibility jika memungkinkan,
5. diuji sebelum dan sesudah refactor,
6. diperbarui dalam dokumen ini.

Perubahan arsitektur tidak dilakukan hanya karena suatu pattern populer atau terlihat lebih kompleks.

Prinsip utamanya:

> Bangun implementasi konkret, pahami polanya, lalu buat abstraksi ketika manfaatnya sudah jelas.
