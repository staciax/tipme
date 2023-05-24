# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from bs4 import BeautifulSoup

from .donate import Donate
from .http import HTTPClient

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self

    from .donate import DonateType as DonatePayload


class TipMeClient:
    def __init__(self) -> None:
        self.http: HTTPClient = HTTPClient()
        self._closed: bool = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]
    ) -> None:
        if self._closed:
            return
        await self.close()

    async def login(self, cookies: Dict[str, str]) -> None:
        await self.http.cookies_login(cookies)

    async def close(self) -> None:
        await self.http.close()

    def is_closed(self) -> bool:
        return self._closed

    async def fetch_latest_donates(self) -> List[Donate]:
        donates: List[Donate] = []
        data = await self.http.get_latest_donates()
        soup = BeautifulSoup(data, "html.parser")
        donate_list = soup.find_all("tr", {"data-token": True})
        for donate in donate_list:
            reference = str(donate).split('data-token="')[1].split('">')[0]
            data = donate.get_text().replace('\t', '').replace('Alert ซ้ำ', '').split('\n')
            data = list(filter(None, data))  # remove empty string
            payload: DonatePayload = {
                'datetime': data[0],
                'author': data[1],
                'amount': data[2],
                'channel': data[3],
                'reference_number': reference,
            }
            if len(data) == 5:
                payload['message'] = data[4]

            donates.append(Donate(payload))

        return donates
