from sqlalchemy.ext.asyncio import AsyncSession

from database.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def add(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        self.session.add(audit_log)

        await self.session.flush()
        await self.session.refresh(audit_log)

        return audit_log