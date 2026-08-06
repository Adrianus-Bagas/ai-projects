from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class TransactionManager:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if exc_type is not None:
            await self.session.rollback()
            return False

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        
        return False