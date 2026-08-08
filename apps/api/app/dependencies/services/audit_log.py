from fastapi import Depends

from app.dependencies.repositories import get_audit_log_repository
from app.repositories.audit_log import AuditLogRepository
from app.services.audit_log import AuditLogService


def get_audit_log_service(
    audit_log_repository: AuditLogRepository = Depends(
        get_audit_log_repository,
    ),
) -> AuditLogService:
    return AuditLogService(
        audit_log_repository=audit_log_repository,
    )