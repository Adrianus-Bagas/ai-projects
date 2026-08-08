from fastapi import Depends

from app.dependencies.repositories import get_user_repository, get_audit_log_repository
from app.dependencies.transaction import get_transaction_manager
from app.repositories.user import UserRepository
from app.repositories.audit_log import AuditLogRepository
from app.services.user import UserService
from app.core.transaction import TransactionManager


def get_user_service(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    audit_log_repository: AuditLogRepository = Depends(
        get_audit_log_repository,
    ),
    transaction_manager: TransactionManager = Depends(
        get_transaction_manager,
    ),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        transaction_manager=transaction_manager,
    )