from clients.base import BaseHTTPClient

class JsonPlaceHolderService:
    """Класс для работы с JSONPlaceholder API"""
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _fetch_json(self, url_path) -> list[dict]:
        async with BaseHTTPClient(self.base_url) as client:
            response = await client.get(url_path=url_path)
            return await response.json()

    async def fetch_users_data(self) -> list[dict]:
        """Получение списка пользователей"""
        return await self._fetch_json(url_path='users')

    async def fetch_posts_data(self) -> list[dict]:
        """Получение списка постов"""
        return await self._fetch_json(url_path='posts')
