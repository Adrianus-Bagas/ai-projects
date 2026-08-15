from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository

from database.models.organization_membership import OrganizationMembership


class OrganizationMembershipRepository(BaseRepository[OrganizationMembership]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session=session,
            model=OrganizationMembership,
        )

    async def get_by_user_and_organization(
        self, 
        user_id: UUID, 
        organization_id: UUID
    ) -> OrganizationMembership | None:
        statement = select(OrganizationMembership).where(
            OrganizationMembership.user_id == user_id,
            OrganizationMembership.organization_id == organization_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
