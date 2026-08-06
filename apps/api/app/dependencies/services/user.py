from fastapi import Depends

from app.dependencies.repositories import get_user_repository
from app.dependencies.transaction import get_transaction_manager
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.core.transaction import TransactionManager


def get_user_service(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    transaction_manager: TransactionManager = Depends(
        get_transaction_manager,
    ),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        transaction_manager=transaction_manager,
    )