from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from fastapi import Depends
from database.session import get_db

async def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)