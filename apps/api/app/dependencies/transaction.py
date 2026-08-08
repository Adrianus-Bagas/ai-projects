from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.transaction import TransactionManager
from app.dependencies.events import get_event_bus
from app.events.bus import EventBus
from database.session import get_db


def get_transaction_manager(
    session: AsyncSession = Depends(get_db),
    event_bus: EventBus = Depends(get_event_bus),
) -> TransactionManager:
    return TransactionManager(
        session=session,
        event_bus=event_bus,
    )