from app.repositories.audit_log import AuditLogRepository
from app.schemas.audit_log_query import (
    AuditLogFilterParams,
    AuditLogSortingParams,
)
from app.schemas.responses.audit_log import AuditLogResponse
from shared.schemas.pagination import (
    PaginatedResponse,
    PaginationMeta,
    PaginationParams,
)


class AuditLogService:
    def __init__(
        self,
        audit_log_repository: AuditLogRepository,
    ) -> None:
        self.audit_log_repository = audit_log_repository

    async def get_audit_logs(
        self,
        pagination: PaginationParams,
        sorting: AuditLogSortingParams,
        filters: AuditLogFilterParams,
    ) -> PaginatedResponse[AuditLogResponse]:
        total_items = await self.audit_log_repository.count(
            filters=filters,
        )

        audit_logs = await self.audit_log_repository.get_paginated(
            pagination=pagination,
            sorting=sorting,
            filters=filters,
        )

        total_pages = (
            total_items + pagination.page_size - 1
        ) // pagination.page_size

        pagination_meta = PaginationMeta(
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=pagination.page < total_pages,
            has_previous=pagination.page > 1,
        )

        return PaginatedResponse[AuditLogResponse](
            items=[
                AuditLogResponse.model_validate(audit_log)
                for audit_log in audit_logs
            ],
            pagination=pagination_meta,
        )