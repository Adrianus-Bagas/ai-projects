from fastapi import APIRouter, Depends

from app.dependencies.services.organization_context import get_current_organization_membership

from database.models.organization_membership import OrganizationMembership

router = APIRouter()

@router.get(
    "/{organization_id}/context",
)
async def get_organization_context(
    membership: OrganizationMembership = Depends(
        get_current_organization_membership
    ),
):

    return {
        "organization_id": membership.organization_id,
        "user_id": membership.user_id,
        "role": membership.role,
    }