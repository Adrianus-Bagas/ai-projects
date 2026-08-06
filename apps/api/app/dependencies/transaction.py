from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.transaction import TransactionManager
from database.session import get_db


def get_transaction_manager(
    session: AsyncSession = Depends(get_db),
) -> TransactionManager:
    return TransactionManager(
        session=session,
    )