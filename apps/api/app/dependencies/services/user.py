from fastapi import Depends

from app.dependencies.repositories import get_user_repository
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_user_service(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
) -> UserService:
    return UserService(
        user_repository=user_repository,
    )