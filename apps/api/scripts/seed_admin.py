import asyncio

from database.session import SessionLocal
from sqlalchemy import select
from database.models.user import User
from auth.password import hash_password


async def seed_admin() -> None:
    async with SessionLocal() as session:
        statement = select(User).where(User.email == 'admin@example.com')
        result = await session.execute(statement)
        admin = result.scalar_one_or_none()
        
        if admin is not None:
            print("Admin sudah ada")
            return
        
        admin = User(
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            name="Admin"
        )
        session.add(admin)
        
        await session.commit()
        
        print("Admin berhasil dibuat")


if __name__ == "__main__":
    asyncio.run(seed_admin())