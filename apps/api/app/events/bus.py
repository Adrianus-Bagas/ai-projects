from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import TypeAlias

from app.events.base import DomainEvent

import logging

logger = logging.getLogger(__name__)

EventHandler: TypeAlias = Callable[
    [DomainEvent],
    Awaitable[None],
]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[
            type[DomainEvent],
            list[EventHandler],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[DomainEvent],
        handler: EventHandler,
    ) -> None:
        self._handlers[event_type].append(handler)

    async def publish(
        self,
        event: DomainEvent,
    ) -> None:
        handlers = self._handlers.get(
            type(event),
            [],
        )

        for handler in handlers:
            try:
                await handler(event)
            except Exception:
                logger.exception(
                    "Event handler failed. event=%s handler=%s event_id=%s",
                    type(event).__name__,
                    getattr(handler, "__name__", repr(handler)),
                    event.event_id,
                )