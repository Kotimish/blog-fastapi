from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import user as schemas


class UsersCRUD:
    """Класс-репозиторий для пользователей"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, new_user: schemas.UserCreateSchema) -> schemas.UserReadSchema:
        user = User(**new_user.model_dump())
        print(user)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return schemas.UserReadSchema.model_validate(user)

    async def get_all(self) -> list[schemas.UserReadSchema]:
        statement = select(User).order_by(User.id)
        result = await self.session.scalars(statement)
        users = result.all()
        return [
            schemas.UserReadSchema.model_validate(user)
            for user in users
        ]

    async def _get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_id(self, user_id: int) -> schemas.UserReadSchema | None:
        user = await self._get_by_id(user_id)
        if not user:
            return None
        return schemas.UserReadSchema.model_validate(user)

    async def update(self, user_id: int, update_user: schemas.UserUpdateSchema) -> schemas.UserReadSchema | None:
        user = await self._get_by_id(user_id)
        if not user:
            return None
        update_data = update_user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return schemas.UserReadSchema.model_validate(user)

    async def delete(self, user_id: int) -> bool:
        user = await self._get_by_id(user_id)
        await self.session.delete(user)
        await self.session.commit()
        return True
