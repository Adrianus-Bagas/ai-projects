from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.dependencies.current_user import get_current_user
from app.services.organization_context import OrganizationContextService
from app.repositories.organization_membership import OrganizationMembershipRepository

from database.models.user import User
from database.models.organization_membership import OrganizationMembership
from database.session import get_db

def get_organization_context_service(
    session: AsyncSession = Depends(get_db),
) -> OrganizationContextService:
    organization_membership_repository = OrganizationMembershipRepository(
        session=session,
    )
    return OrganizationContextService(
        organization_membership_repository=organization_membership_repository,
    )

async def get_current_organization_membership(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    organization_context_service: OrganizationContextService = Depends(get_organization_context_service),
) -> OrganizationMembership:
    return await organization_context_service.get_membership_context(
        organization_id=organization_id,
        user_id=current_user.id,
    )