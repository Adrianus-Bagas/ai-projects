import asyncio
from uuid import UUID

from sqlalchemy.orm.exc import StaleDataError

from app.repositories.user import UserRepository
from database.session import SessionLocal
from app.core.transaction import TransactionManager

async def test_optimistic_locking(
    user_id: UUID,
) -> None:
    async with SessionLocal() as session_a:
        async with SessionLocal() as session_b:
            repository_a = UserRepository(session=session_a)
            repository_b = UserRepository(session=session_b)

            user_a = await repository_a.get_by_id(
                entity_id=user_id,
            )
            user_b = await repository_b.get_by_id(
                entity_id=user_id,
            )

            if user_a is None or user_b is None:
                raise ValueError("User not found")

            print(
                "Initial versions:",
                user_a.version,
                user_b.version,
            )

            user_a.name = f"{user_a.name} A"

            await repository_a.save(user_a)
            await repository_a.commit()

            print(
                "Session A committed:",
                user_a.version,
            )

            user_b.name = f"{user_b.name} B"
            
            transaction_manager_b = TransactionManager(
                session=session_b,
            )

            try:
                async with transaction_manager_b:
                    await repository_b.save(
                        entity=user_b,
                    )
            except StaleDataError:
                print(
                    "Optimistic locking worked and "
                    "TransactionManager handled rollback."
                )
                session_b.expire_all()

                fresh_user = await repository_b.get_by_id(
                    entity_id=user_id,
                )
            
                if fresh_user is None:
                    raise ValueError("User not found after rollback")
            
                print(
                    "Session B usable after rollback:",
                    fresh_user.version,
                )
            else:
                print(
                    "Unexpected: Session B update succeeded."
                )

async def main() -> None:
    user_id = UUID(
        "a16484d3-d9a2-4641-b8f0-c9c68ebfa642"
    )

    await test_optimistic_locking(
        user_id=user_id,
    )


if __name__ == "__main__":
    asyncio.run(main())