import asyncio
from uuid import UUID

from sqlalchemy.orm.exc import StaleDataError

from app.repositories.user import UserRepository
from database.session import SessionLocal

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

            try:
                await repository_b.save(user_b)
                await repository_b.commit()
            except StaleDataError:
                await repository_b.rollback()

                print(
                    "Optimistic locking worked: "
                    "Session B used a stale version."
                )
            else:
                print(
                    "Unexpected: Session B commit succeeded."
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