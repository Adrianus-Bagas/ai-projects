from fastapi import APIRouter, Depends
from uuid import UUID
from typing import Annotated

from app.dependencies.services.user import get_user_service
from app.dependencies.require_roles import require_roles
from app.schemas.responses.user import UserResponse, UpdateUserRoleRequest
from app.services.user import UserService

from database.models.user import User, UserRole
from shared.responses import ApiResponse
from shared.schemas import (
    PaginatedResponse,
    PaginationParams,
    UserSortingParams,
)

router = APIRouter()


@router.get(
    "",
    response_model=ApiResponse[
        PaginatedResponse[UserResponse]
    ],
)
async def get_users(
    pagination: Annotated[
        PaginationParams,
        Depends(),
    ],
    sorting: Annotated[
        UserSortingParams,
        Depends(),
    ],
    _: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    user_service: UserService = Depends(
        get_user_service,
    ),
) -> ApiResponse[PaginatedResponse[UserResponse]]:
    user_data = await user_service.get_all_users(
        pagination=pagination,
        sorting=sorting,
    )
    return ApiResponse[PaginatedResponse[UserResponse]](
        data=user_data,
        success=True,
        message="Users retrieved successfully",
    )

@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
)
async def get_user_by_id(
    user_id: UUID,
    _: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    user_service: UserService = Depends(
        get_user_service,
    ),
) -> ApiResponse[UserResponse]:
    user = await user_service.get_user_by_id(
        user_id=user_id,
    )

    return ApiResponse[UserResponse](
        success=True,
        message="Get user success",
        data=user,
    )

@router.patch(
    "/users/{user_id}/role",
    response_model=ApiResponse[UserResponse],
)
async def update_user_role(
    user_id: UUID,
    request: UpdateUserRoleRequest,
    current_user: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    user_service: UserService = Depends(
        get_user_service,
    ),
) -> ApiResponse[UserResponse]:
    user = await user_service.update_user_role(
        user_id=user_id,
        role=request.role,
        current_user=current_user
    )

    return ApiResponse[UserResponse](
        success=True,
        message="Update user role success",
        data=user,
    )