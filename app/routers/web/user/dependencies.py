from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from routers.dependencies import get_async_session
from repositories.user import UsersCRUD


async def get_users_crud(
    session: AsyncSession = Depends(get_async_session)
):
    return UsersCRUD(session)
