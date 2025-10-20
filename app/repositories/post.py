from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Post
from schemas import post as schemas


class PostsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, new_post: schemas.PostCreateSchema) -> schemas.PostReadSchema:
        post = Post(**new_post.model_dump())
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return schemas.PostReadSchema.model_validate(post)

    async def get_all(self) -> list[schemas.PostReadSchema]:
        statement = select(Post).options(selectinload(Post.user)).order_by(Post.id)
        result = await self.session.scalars(statement)
        posts = result.all()
        return [
            schemas.PostReadSchema.model_validate(post)
            for post in posts
        ]

    async def _get_by_id(self, post_id: int) -> Post | None:
        return await self.session.get(Post, post_id)

    async def get_by_id(self, post_id: int) -> schemas.PostReadSchema | None:
        post = await self._get_by_id(post_id)
        if not post:
            return None
        return schemas.PostReadSchema.model_validate(post)

    async def get_with_user_by_id(self, post_id: int) -> schemas.PostWithUserReadSchema | None:
        statement = (
            select(Post)
            .where(
                Post.id == post_id
            )
            .options(
                selectinload(Post.user)
            )
            .order_by(Post.id)
        )
        result = await self.session.execute(statement)
        post = result.scalar_one_or_none()
        if not post:
            return None
        return schemas.PostWithUserReadSchema.model_validate(post)

    async def update(self, post_id: int, update_post: schemas.PostUpdateSchema) -> schemas.PostReadSchema | None:
        post = await self._get_by_id(post_id)
        if not post:
            return None
        update_data = update_post.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)
        await self.session.commit()
        await self.session.refresh(post)
        return schemas.PostReadSchema.model_validate(post)

    async def delete(self, post_id: int) -> bool:
        post = await self._get_by_id(post_id)
        if not post:
            return False
        await self.session.delete(post)
        await self.session.commit()
        return True
