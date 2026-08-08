import asyncio
from uuid import uuid4

from app.events.bus import EventBus
from app.events.user import UserRoleChanged
from database.models.enums import UserRole


async def handle_user_role_changed(
    event: UserRoleChanged,
) -> None:
    print(
        "Handler received:",
        event.user_id,
        event.old_role,
        "->",
        event.new_role,
    )


async def main() -> None:
    event_bus = EventBus()

    event_bus.subscribe(
        UserRoleChanged,
        handle_user_role_changed,
    )

    event = UserRoleChanged(
        actor_id=uuid4(),
        user_id=uuid4(),
        old_role=UserRole.USER,
        new_role=UserRole.ADMIN,
    )

    await event_bus.publish(event)


if __name__ == "__main__":
    asyncio.run(main())