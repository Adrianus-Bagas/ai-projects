from database.models.user import User
from app.repositories.user_repository import UserRepository
from shared.errors.exceptions import AppException
from shared.errors.constants import SharedErrorCode, USER_NOT_FOUND_ERROR_MESSAGE

from http import HTTPStatus

from uuid import UUID


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