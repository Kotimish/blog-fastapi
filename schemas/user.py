from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserCreateSchema(UserBaseSchema):
    """
    Схема создания нового пользователя
    """


class UserReadSchema(UserBaseSchema):
    """
    Схема чтения пользователя
    """
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime


class UserUpdateSchema(BaseModel):
    """
    Схема обновления пользователя
    """
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
