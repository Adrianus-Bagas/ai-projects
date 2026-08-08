from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.events.base import DomainEvent


class TransactionManager:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self._pending_events: list[DomainEvent] = []
        self._committed_events: list[DomainEvent] = []

    @property
    def commited_events(self) -> tuple[DomainEvent, ...]:
        return tuple(self._committed_events)

    def add_event(
        self,
        event: DomainEvent,
    ) -> None:
        self._pending_events.append(event)

    def clear_events(self) -> None:
        self._pending_events.clear()

    async def __aenter__(self) -> Self:
        self._pending_events.clear()
        self._committed_events.clear()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if exc_type is not None:
            await self.session.rollback()
            self._pending_events.clear()
            self._committed_events.clear()
            return False

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            self._pending_events.clear()
            self._committed_events.clear()
            raise
        
        self._committed_events = self._pending_events.copy()
        self._pending_events.clear()
        
        return False