from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import func, select

from app.schemas.audit_log_query import AuditLogFilterParams
from app.schemas.audit_log_query import (
    AuditLogFilterParams,
    AuditLogSortingParams,
    AuditLogSortField,
)

from shared.schemas.pagination import PaginationParams
from shared.schemas.sorting import SortOrder
from database.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        
    def _build_filters(
        self,
        filters: AuditLogFilterParams,
    ) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []

        if filters.action is not None:
            conditions.append(
                AuditLog.action == filters.action
            )

        if filters.entity_type is not None:
            conditions.append(
                AuditLog.entity_type == filters.entity_type
            )

        if filters.actor_id is not None:
            conditions.append(
                AuditLog.actor_id == filters.actor_id
            )

        if filters.entity_id is not None:
            conditions.append(
                AuditLog.entity_id == filters.entity_id
            )

        if filters.event_name is not None:
            conditions.append(
                AuditLog.event_name == filters.event_name
            )

        return conditions

    async def add(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        self.session.add(audit_log)

        await self.session.flush()
        await self.session.refresh(audit_log)

        return audit_log
    
    async def count(
        self,
        filters: AuditLogFilterParams,
    ) -> int:
        conditions = self._build_filters(filters)

        statement = (
            select(func.count())
            .select_from(AuditLog)
            .where(*conditions)
        )

        result = await self.session.execute(statement)

        return result.scalar_one()

    async def get_paginated(
        self,
        pagination: PaginationParams,
        sorting: AuditLogSortingParams,
        filters: AuditLogFilterParams,
    ) -> list[AuditLog]:
        conditions = self._build_filters(filters)
    
        sort_columns = {
            AuditLogSortField.CREATED_AT: AuditLog.created_at,
            AuditLogSortField.ACTION: AuditLog.action,
            AuditLogSortField.ENTITY_TYPE: AuditLog.entity_type,
            AuditLogSortField.EVENT_NAME: AuditLog.event_name,
        }
    
        sort_column = sort_columns[sorting.sort_by]
    
        order_expression = (
            sort_column.asc()
            if sorting.sort_order == SortOrder.ASC
            else sort_column.desc()
        )
    
        statement = (
            select(AuditLog)
            .where(*conditions)
            .order_by(
                order_expression,
                AuditLog.id.asc(),
            )
            .limit(pagination.page_size)
            .offset(pagination.offset)
        )
    
        result = await self.session.execute(statement)
    
        return list(result.scalars().all())