from http import HTTPStatus
from uuid import UUID

from app.repositories.organization_membership import (
    OrganizationMembershipRepository, 
)

from database.models.organization_membership import (
    OrganizationMembership, 
)
from shared.errors.constants import (
    SharedErrorCode,
    NOT_IN_ORGANIZATION,
    
)
from shared.errors.exceptions import AppException


class OrganizationContextService:
    def __init__(
        self,
        organization_membership_repository: OrganizationMembershipRepository,
    ) -> None:
        self.organization_membership_repository = organization_membership_repository
        
    async def get_membership_context(
        self,
        user_id: UUID,
        organization_id: UUID,
    ) -> OrganizationMembership:
        
        membership = await self.organization_membership_repository.get_by_user_and_organization(
            user_id=user_id,
            organization_id=organization_id
        )
        
        if membership is None:
            raise AppException(
                status_code=HTTPStatus.FORBIDDEN,
                message=NOT_IN_ORGANIZATION,
                error_code=SharedErrorCode.NOT_IN_ORGANIZATION,
            )
        
        return membership
