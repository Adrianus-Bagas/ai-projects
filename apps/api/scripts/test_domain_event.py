import asyncio
from uuid import uuid4

from app.core.transaction import TransactionManager
from app.events.base import DomainEvent
from app.events.user import UserRoleChanged
from app.events.bus import EventBus
from database.models.enums import UserRole
from database.session import SessionLocal

async def handle_user_role_changed(
    event: DomainEvent,
) -> None:
    print(
        "EventBus received:",
        type(event).__name__,
    )

async def successful_handler(
    event: DomainEvent,
) -> None:
    print(
        "Successful handler received:",
        type(event).__name__,
    )

async def failing_handler(
    event: DomainEvent,
) -> None:
    print(
        "Failing handler received:",
        type(event).__name__,
    )

    raise RuntimeError(
        "Simulated event handler failure"
    )

async def test_committed_event() -> None:
    async with SessionLocal() as session:
        
        event_bus = EventBus()
        
        event_bus.subscribe(
            UserRoleChanged,
            failing_handler,
        )
        
        event_bus.subscribe(
            UserRoleChanged,
            successful_handler,
        )
        
        transaction_manager = TransactionManager(
            session=session,
            event_bus=event_bus,
        )

        event = UserRoleChanged(
            actor_id=uuid4(),
            user_id=uuid4(),
            old_role=UserRole.USER,
            new_role=UserRole.ADMIN,
        )

        try:
            async with transaction_manager:
                transaction_manager.add_event(event)
        except RuntimeError as exc:
            print(
                "Handler error:",
                exc,
            )

        print(
            "After commit:",
            transaction_manager.commited_events,
        )

async def test_rollback_discards_event() -> None:
    async with SessionLocal() as session:
        event_bus = EventBus()
        
        event_bus.subscribe(
            UserRoleChanged,
            failing_handler,
        )
        
        transaction_manager = TransactionManager(
            session=session,
            event_bus=event_bus,
        )

        event = UserRoleChanged(
            actor_id=uuid4(),
            user_id=uuid4(),
            old_role=UserRole.USER,
            new_role=UserRole.ADMIN,
        )

        try:
            async with transaction_manager:
                transaction_manager.add_event(event)

                raise RuntimeError(
                    "Simulated transaction failure"
                )
        except RuntimeError:
            pass

        print(
            "After rollback:",
            transaction_manager.commited_events,
        )


async def main() -> None:
    await test_committed_event()
    await test_rollback_discards_event()


if __name__ == "__main__":
    asyncio.run(main())