from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


# --- Маппинг: внешний API во внутреннюю структуру ---
def map_jsonplaceholder_user(user_data: dict) -> dict:
    return {
        "id": user_data["id"],
        "full_name": user_data["name"],
        "username": user_data["username"],
        "email": user_data["email"],
    }


# --- Сидер: работа с БД ---
# TODO Важно сделать синхронизацию при ручнос заполнении id
class RawUserRepository:
    """Класс репозиторий для работы с сырыми данными пользователей без схем"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self) -> list[User]:
        statement = select(User).order_by(User.id)
        result = await self.session.scalars(statement)
        return list(result.all())

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        return user

    async def create_many(self, users_data: list[dict]) -> list[User]:
        users = [
            User(**user_data)
            for user_data in users_data
        ]
        self.session.add_all(users)
        await self.session.commit()
        return users
