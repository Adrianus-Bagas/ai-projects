import asyncio
from uuid import uuid4

from app.core.transaction import TransactionManager
from app.events.user import UserRoleChanged
from database.models.enums import UserRole
from database.session import SessionLocal


async def test_committed_event() -> None:
    async with SessionLocal() as session:
        transaction_manager = TransactionManager(
            session=session,
        )

        event = UserRoleChanged(
            actor_id=uuid4(),
            user_id=uuid4(),
            old_role=UserRole.USER,
            new_role=UserRole.ADMIN,
        )

        async with transaction_manager:
            transaction_manager.add_event(event)

            print(
                "Inside transaction:",
                transaction_manager.commited_events,
            )

        print(
            "After commit:",
            transaction_manager.commited_events,
        )

async def test_rollback_discards_event() -> None:
    async with SessionLocal() as session:
        transaction_manager = TransactionManager(
            session=session,
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