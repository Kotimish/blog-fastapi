import asyncio
from typing import Optional, Union

import aiohttp
from yarl import URL


class BaseHTTPClient:
    """Базовый класс для HTTP-запросов"""

    def __init__(self, url: str | URL):
        self.base_url: URL = url if isinstance(url, URL) else URL(url)
        self._session: Optional[aiohttp.ClientSession] = None
        self._default_timeout = 5

    async def __aenter__(self) -> 'BaseHTTPClient':
        self._session = aiohttp.ClientSession(base_url=self.base_url)
        return self

    async def __aexit__(self, *args) -> None:
        await self._session.close()
        self._session = None

    async def _request(self, method, url_path, timeout: Optional[int] = None, **kwargs) -> aiohttp.ClientResponse:
        if timeout is None:
            timeout = self._default_timeout
        async with asyncio.timeout(timeout):
            response = await self._session.request(method, url_path, **kwargs)
            response.raise_for_status()
            return response

    async def get(self, url_path: str, timeout: Optional[int] = None, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('GET', url_path, timeout, **kwargs)

    async def post(self, url_path: str, data: dict, timeout: Optional[int] = None, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('POST', url_path, timeout, json=data, **kwargs)

    async def put(self, url_path: str, data: dict, timeout: Optional[int] = None, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('PUT', url_path, timeout, json=data, **kwargs)

    async def patch(self, url_path: str, data: dict, timeout: Optional[int] = None, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('PATCH', url_path, timeout, json=data, **kwargs)

    async def delete(self, url_path: str, timeout: Optional[int] = None, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('DELETE', url_path, timeout, **kwargs)
