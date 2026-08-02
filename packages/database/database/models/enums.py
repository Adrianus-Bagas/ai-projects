from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"

class AuditAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RESTORE = "restore"