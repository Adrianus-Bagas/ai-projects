from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User
from shared.schemas.pagination import PaginationParams


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[User]:
        statement = select(User).order_by(
            User.created_at.desc(),
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())
    
    async def count(self) -> int:
        statement = select(func.count()).select_from(User)
        result = await self.session.execute(statement)
        return result.scalar_one()
    
    async def get_paginated(
        self, 
        pagination: PaginationParams
    ) -> list[User]:
        statement = (
            select(User)
            .order_by(User.created_at.desc())
            .limit(pagination.page_size)
            .offset(pagination.offset)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def save(
        self,
        user: User,
    ) -> User:
        await self.session.flush()
        await self.session.refresh(user)

        return user
    
    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()