# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, Optional

import bs4.element
from bs4 import BeautifulSoup

from .donate import Donate
from .http import HTTPClient
from .user import User

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self

    from .donate import DonateType as DonatePayload
    from .user import UserType as UserPayload

_log = logging.getLogger(__name__)


class TipMeClient:
    def __init__(self) -> None:
        self.http: HTTPClient = HTTPClient()
        self._closed: bool = False
        self.user: Optional[User] = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]
    ) -> None:
        if self._closed:
            return
        await self.close()

    async def login(self, cookies: Dict[str, str]) -> None:
        data = await self.http.cookies_login(cookies)
        soup = BeautifulSoup(data, 'html.parser')

        # username

        id_username = soup.find('input', id='id_username')
        if id_username is None or isinstance(id_username, bs4.element.NavigableString):
            raise ValueError('Invalid cookies')
        username = id_username.get('value')

        # email

        email_id = soup.find('input', id='id_email')
        if email_id is None or isinstance(email_id, bs4.element.NavigableString):
            raise ValueError('Invalid cookies')

        email = email_id.get('value')

        payload: UserPayload = {'username': str(username), 'email': str(email)}
        self.user = User(payload)

        # email alert?

        _log.info(f'Logged in as {self.user.username!r}')

    async def close(self) -> None:
        await self.http.close()

    def is_closed(self) -> bool:
        return self._closed

    async def fetch_latest_donates(self) -> List[Donate]:
        donates: List[Donate] = []
        data = await self.http.get_latest_donates()
        soup = BeautifulSoup(data, 'html.parser')
        donate_list = soup.find_all('tr', {'data-token': True})  # find all donate
        for donate in donate_list:
            reference = str(donate).split('data-token="')[1].split('">')[0]  # get reference number
            data = donate.get_text().replace('\t', '').replace('Alert ซ้ำ', '').split('\n')  # remove tab and alert
            data = list(filter(None, data))  # remove empty string
            datetime, author, amount, channel, *message = data  # unpack data
            payload: DonatePayload = {
                'datetime': datetime,
                'author': author,
                'amount': amount,
                'channel': channel,
                'reference_number': reference,
            }
            if message:
                payload['message'] = message[0]

            donates.append(Donate(payload))

        return donates
