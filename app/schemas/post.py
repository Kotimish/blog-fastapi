from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.user import UserReadSchema


class PostBaseSchema(BaseModel):
    title: str
    body: str | None = None


class PostCreateSchema(PostBaseSchema):
    """
    Схема создания нового поста
    """
    user_id: int


class PostReadSchema(PostBaseSchema):
    """
    Схема чтения поста
    """
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    user_id: int
    created_at: datetime

class PostWithUserReadSchema(PostBaseSchema):
    """
    Схема чтения поста со ссылкой на пользователя
    """
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    user_id: int
    user: UserReadSchema
    created_at: datetime


class PostUpdateSchema(BaseModel):
    """
    Схема обновления поста
    """
    title: str | None = None
    body: str | None = None
