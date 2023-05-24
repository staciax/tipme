# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, ClassVar, Coroutine, Dict, Optional, TypeVar, Union

import aiohttp

from .errors import HTTPException, InternalServerError, NotFound

if TYPE_CHECKING:
    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]

# inspired by https://github.com/Rapptz/discord.py/blob/master/http.py


class Route:
    BASE: ClassVar[str] = 'https://tipme.in.th'

    def __init__(
        self,
        method: str,
        path: str,
        **parameters: Any,
    ) -> None:
        self.method = method
        self.path = path
        self.parameters = parameters
        self.url: str = self.BASE + self.path


class HTTPClient:
    def __init__(self) -> None:
        self.__session: Optional[aiohttp.ClientSession] = None

    async def cookies_login(self, cookies: Dict[str, str]) -> None:
        self.__session = aiohttp.ClientSession(cookies=cookies)

    async def close(self) -> None:
        if self.__session:
            await self.__session.close()

    async def request(self, method: str, url: str, allow_redirects: bool = False, **kwargs: Any) -> Any:
        if self.__session is None:
            raise RuntimeError('You must login first. use TipMeClient.login()')

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        for tries in range(5):
            try:
                async with self.__session.request(method, url, **kwargs) as response:
                    data = await response.text()
                    if response.status == 200:
                        return data
                    elif response.status == 404:
                        raise NotFound(f'HTTP error {response.status} {response.reason}: {data}')
                    elif response.status >= 500:
                        raise InternalServerError(f'HTTP error {response.status} {response.reason}: {data}')

            except OSError as e:
                if tries < 4 and e.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response is not None:
            # We've run out of retries, raise.
            if response.status >= 500:
                raise InternalServerError(f'HTTP error {response.status} {response.reason} (retrying): {data}')
            raise HTTPException(f'HTTP error {response.status} {response.reason}: {data}')
        raise RuntimeError('Unreachable code in HTTP handling')

    def get_latest_donates(self) -> Response[Any]:
        r = Route('GET', '/tx')
        return self.request(r.method, r.url)

    def get_statistics(self) -> Response[Any]:
        r = Route('GET', '/tx/stats')
        return self.request(r.method, r.url)

    def get_transaction(self) -> Response[Any]:
        r = Route('GET', '/tx/list_tx')
        return self.request(r.method, r.url)

    def get_receipt(self) -> Response[Any]:
        r = Route('GET', '/tx/invoices')
        return self.request(r.method, r.url)

    def withdraw_money(self) -> Response[Any]:
        r = Route('GET', '/tx/withdraw')
        return self.request(r.method, r.url)

    def get_user(self) -> Response[Any]:
        r = Route('GET', '/user')
        return self.request(r.method, r.url)

    def get_payment(self) -> Response[Any]:
        r = Route('GET', '/payments')
        return self.request(r.method, r.url)
