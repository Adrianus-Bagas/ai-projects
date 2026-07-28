from http import HTTPStatus
from fastapi import Depends

from database.models.enums import UserRole
from database.models.user import User

from app.dependencies.current_user import get_current_active_user

from shared.errors import AppException
from auth.constants import AuthErrorCode

from collections.abc import Awaitable, Callable


def require_roles(
    *roles: UserRole,
) -> Callable[..., Awaitable[User]]:
    if not roles:
        raise ValueError(
            "At least one role must be provided"
        )
    async def dependency(
        current_user: User = Depends(
            get_current_active_user,
        ),
    ) -> User:
        if(current_user.role not in roles):
            raise AppException(
                status_code=HTTPStatus.FORBIDDEN,
                error_code=AuthErrorCode.INSUFFICIENT_PERMISSIONS,
                message="Insufficient permissions"
            )
        return current_user

    return dependency