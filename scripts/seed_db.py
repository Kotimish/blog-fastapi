import asyncio

from clients import JsonPlaceHolderService
from core.config import settings
from core.db_async import async_session
from seeders.post import RawPostRepository, map_jsonplaceholder_post
from seeders.user import RawUserRepository, map_jsonplaceholder_user


async def init_data():
    """Заполнение базы данных данными"""
    # Загрузка данных из внешнего API
    base_url = settings.jsonplaceholder.base_url
    client = JsonPlaceHolderService(base_url=str(base_url))
    raw_users_data, raw_posts_data = await asyncio.gather(
        client.fetch_users_data(),
        client.fetch_posts_data(),
    )
    # Конвертация данных
    users_data = [
        map_jsonplaceholder_user(user_data)
        for user_data in raw_users_data
    ]
    posts_data = [
        map_jsonplaceholder_post(post_data)
        for post_data in raw_posts_data
    ]
    # Сохранение в БД
    async with async_session() as session:
        user_crud = RawUserRepository(session)
        post_crud = RawPostRepository(session)
        await user_crud.create_many(users_data)
        await post_crud.create_many(posts_data)


if __name__ == "__main__":
    asyncio.run(init_data())
