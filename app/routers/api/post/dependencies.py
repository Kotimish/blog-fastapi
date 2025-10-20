from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from routers.dependencies import get_async_session
from repositories.post import PostsCRUD


async def get_posts_crud(
    session: AsyncSession = Depends(get_async_session)
):
    return PostsCRUD(session)
