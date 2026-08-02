from uuid import UUID

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from.base import BaseRepository

from database.models.user import User
from shared.schemas import (
    PaginationParams, 
    UserSortingParams, 
    SortOrder, 
    UserSortField, 
    UserFilterParams,
)


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session=session,
            model=User,
        )

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def count(
        self,
        filters: UserFilterParams,
    ) -> int:
        conditions = self._build_filters(filters)
        
        statement = (
            select(func.count())
            .select_from(User)
            .where(*conditions)
        )
        
        result = await self.session.execute(statement)
        return result.scalar_one()
    
    async def get_paginated(
        self, 
        pagination: PaginationParams,
        sorting: UserSortingParams,
        filters: UserFilterParams,
    ) -> list[User]:
        conditions = self._build_filters(filters)
        
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
            .where(*conditions)
            .order_by(
                order_expression,
                User.id.asc(),
            )
            .limit(pagination.page_size)
            .offset(pagination.offset)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    def _build_filters(
            self,
            filters: UserFilterParams,
    ) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []

        if filters.role is not None:
            conditions.append(User.role == filters.role)

        if filters.is_active is not None:
            conditions.append(User.is_active == filters.is_active)
            
        if filters.search is not None:
            search_pattern = f"%{filters.search}%"
            conditions.append(
                or_(
                    User.name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                )
            )
            
        return conditions