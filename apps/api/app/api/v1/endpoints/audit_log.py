from fastapi import APIRouter, Depends

from app.dependencies.require_roles import require_roles
from app.dependencies.services.audit_log import get_audit_log_service
from app.schemas.audit_log_query import (
    AuditLogFilterParams,
    AuditLogSortingParams,
)
from app.schemas.responses.audit_log import AuditLogResponse
from app.services.audit_log import AuditLogService
from database.models.enums import UserRole
from database.models.user import User
from shared.responses import ApiResponse
from shared.schemas.pagination import (
    PaginatedResponse,
    PaginationParams,
)


router = APIRouter()


@router.get(
    "",
    response_model=ApiResponse[
        PaginatedResponse[AuditLogResponse]
    ],
)
async def get_audit_logs(
    pagination: PaginationParams = Depends(),
    sorting: AuditLogSortingParams = Depends(),
    filters: AuditLogFilterParams = Depends(),
    _: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    audit_log_service: AuditLogService = Depends(
        get_audit_log_service,
    ),
) -> ApiResponse[PaginatedResponse[AuditLogResponse]]:
    audit_logs = await audit_log_service.get_audit_logs(
        pagination=pagination,
        sorting=sorting,
        filters=filters,
    )

    return ApiResponse[PaginatedResponse[AuditLogResponse]](
        success=True,
        message="Audit logs retrieved successfully",
        data=audit_logs,
    )