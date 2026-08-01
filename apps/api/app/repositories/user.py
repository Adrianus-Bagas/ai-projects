from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User
from shared.schemas import PaginationParams, UserSortingParams, SortOrder, UserSortField


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
        pagination: PaginationParams,
        sorting: UserSortingParams,
    ) -> list[User]:
        
        sort_columns = {
            UserSortField.CREATED_AT: User.created_at,
            UserSortField.NAME: User.name,
            UserSortField.EMAIL: User.email,
            UserSortField.ROLE: User.role,
        }
        
        sort_column = sort_columns[sorting.sort_by]
        
        order_expression = (
            sort_column.asc()
            if sorting.sort_order == SortOrder.ASC
            else sort_column.desc()
        )
        
        statement = (
            select(User)
            .order_by(
                order_expression,
                User.id.asc(),
            )
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