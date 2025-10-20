from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from core.db_async import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
