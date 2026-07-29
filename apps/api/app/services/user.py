from http import HTTPStatus
from uuid import UUID

from app.repositories.user import UserRepository
from database.models.enums import UserRole
from database.models.user import User
from shared.errors.constants import (
    CANNOT_CHANGE_OWN_ROLE_ERROR_MESSAGE,
    USER_NOT_FOUND_ERROR_MESSAGE,
    SharedErrorCode,
)
from shared.errors.exceptions import AppException


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all()

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.user_repository.get_by_id(
            user_id=user_id,
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

        try:
            user.role = role

            updated_user = await self.user_repository.save(
                user=user,
            )

            await self.user_repository.commit()

            return updated_user
        except Exception:
            await self.user_repository.rollback()
            raise