from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Post


# --- Маппинг: внешний API во внутреннюю структуру ---
def map_jsonplaceholder_post(post_data: dict) -> dict:
    return {
        "id": post_data["id"],
        "title": post_data["title"],
        "body": post_data["body"],
        "user_id": post_data["userId"],
    }


# --- Сидер: работа с БД ---
class RawPostRepository:
    """Класс репозиторий для работы с сырыми данными постов без схем"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self) -> list[Post]:
        statement = select(Post).order_by(Post.id)
        result = await self.session.scalars(statement)
        return list(result.all())

    async def get_by_id(self, post_id: int) -> Post | None:
        return await self.session.get(Post, post_id)

    async def create(self, post_data: dict) -> Post:
        post = Post(**post_data)
        self.session.add(post)
        await self.session.commit()
        return post

    async def create_many(self, posts_data: list[dict]) -> list[Post]:
        posts = [
            Post(**post_data)
            for post_data in posts_data
        ]
        self.session.add_all(posts)
        await self.session.commit()
        return posts
