from http import HTTPStatus
from uuid import UUID

from app.repositories.user import UserRepository
from app.repositories.audit_log import AuditLogRepository
from app.schemas.responses.user import UserResponse
from app.core.transaction import TransactionManager
from app.events.user import UserRoleChanged

from database.models.enums import UserRole, AuditAction
from database.models.user import User
from database.models.audit_log import AuditLog
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
)
from app.schemas.user_query import (
    UserFilterParams, 
    UserSortingParams,
)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        audit_log_repository: AuditLogRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self.user_repository = user_repository
        self.audit_log_repository = audit_log_repository
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
        
        pagination_meta = PaginationMeta.create(
            pagination=pagination,
            total_items=total_items,
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
        
        if user.role == role:
            return user
        
        old_role = user.role
        
        async with self.transaction_manager:
            user.role = role
            
            updated_user = await self.user_repository.save(
                entity=user,
            )
            
            audit_log = AuditLog(
                actor_id=current_user.id,
                action=AuditAction.UPDATE,
                entity_type="user",
                entity_id=user.id,
                event_name="user.role_change",
                changes={
                    "role": {
                        "old": old_role.value,
                        "new": role.value,
                    }
                },
            )
            
            await self.audit_log_repository.add(
                audit_log=audit_log,
            )
            
            self.transaction_manager.add_event(
                UserRoleChanged(
                    actor_id=current_user.id,
                    user_id=user.id,
                    old_role=old_role,
                    new_role=role,
                )
            )
        
        return updated_user        