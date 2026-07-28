import asyncio

from database.session import SessionLocal
from sqlalchemy import select
from database.models.user import User
from database.models.enums import UserRole
from auth.password import hash_password


async def seed_user() -> None:
    async with SessionLocal() as session:
        statement = select(User).where(User.email == 'user@example.com')
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        
        if user is not None:
            print("User sudah ada")
            return
        
        user = User(
            email="user@example.com",
            password_hash=hash_password("user123"),
            name="User",
            role=UserRole.USER
        )
        session.add(user)
        
        await session.commit()
        
        print("User berhasil dibuat")


if __name__ == "__main__":
    asyncio.run(seed_user())