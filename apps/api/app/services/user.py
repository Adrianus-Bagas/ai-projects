from http import HTTPStatus
from uuid import UUID

from app.repositories.user import UserRepository
from app.schemas.responses.user import UserResponse
from app.core.transaction import TransactionManager

from database.models.enums import UserRole
from database.models.user import User
from shared.errors.constants import (
    CANNOT_CHANGE_OWN_ROLE_ERROR_MESSAGE,
    USER_NOT_FOUND_ERROR_MESSAGE,
    SharedErrorCode,
)
from shared.errors.exceptions import AppException
from shared.schemas import (
    PaginationParams,
    PaginationMeta,
    PaginatedResponse,
    UserSortingParams,
    UserFilterParams,
)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    async def get_all_users(
        self,
        pagination: PaginationParams,
        sorting: UserSortingParams,
        filters: UserFilterParams,
    ) -> PaginatedResponse[UserResponse]:
        total_items = await self.user_repository.count(
            filters=filters,
        )
        
        users = await self.user_repository.get_paginated(
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
        
        return PaginatedResponse[UserResponse](
            items=[
                UserResponse.model_validate(user)
                for user in users
            ],
            pagination=pagination_meta,
        )

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.user_repository.get_by_id(
            entity_id=user_id,
        )

        if user is None:
            raise AppException(
                status_code=HTTPStatus.NOT_FOUND,
                message=USER_NOT_FOUND_ERROR_MESSAGE,
                error_code=SharedErrorCode.USER_NOT_FOUND,
            )

        return user

    async def update_user_role(
        self,
        user_id: UUID,
        role: UserRole,
        current_user: User,
    ) -> User:
        user = await self.get_user_by_id(
            user_id=user_id,
        )

        if user.id == current_user.id:
            raise AppException(
                status_code=HTTPStatus.FORBIDDEN,
                message=CANNOT_CHANGE_OWN_ROLE_ERROR_MESSAGE,
                error_code=SharedErrorCode.CANNOT_CHANGE_OWN_ROLE,
            )
        
        async with self.transaction_manager:
            user.role = role
            
            updated_user = await self.user_repository.save(
                entity=user,
            )
        
        return updated_user        