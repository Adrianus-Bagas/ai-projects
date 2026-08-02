from typing import Generic, TypeVar
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
    ) -> None:
        self.session = session
        self.model = model

    async def get_by_id(
        self,
        entity_id: UUID,
    ) -> ModelType | None:
        statement = select(self.model).where(
            self.model.id == entity_id,
            self.model.deleted_at.is_(None),
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id_including_deleted(
        self,
        entity_id: UUID,
    ) -> ModelType | None:
        statement = select(self.model).where(
            self.model.id == entity_id,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[ModelType]:
        statement = select(self.model)

        result = await self.session.execute(statement)

        return list(result.scalars().all())
    
    def add(
        self,
        entity: ModelType,  
    ) -> None:
        self.session.add(entity)
        
    async def delete(
        self,
        entity: ModelType,
    ) -> ModelType:
        entity.deleted_at = datetime.now(timezone.utc)

        await self.session.flush()
        await self.refresh(entity)

        return entity
    
    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(
        self,
        entity: ModelType,
    ) -> None:
        await self.session.refresh(entity)
    
    async def save(
        self,
        entity: ModelType,
    ) -> ModelType:
        self.add(entity)
    
        await self.session.flush()
        await self.refresh(entity)
    
        return entity