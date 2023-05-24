# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

from __future__ import annotations

import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from tipme import TipMeClient

load_dotenv()

if os.getenv('SESSION_ID') is None:
    raise RuntimeError('SESSION_ID is not set.')


@pytest.fixture(scope='session')
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # policy = asyncio.get_event_loop_policy()
        # loop = policy.new_event_loop()
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TipMeClient, None]:
    async with TipMeClient() as client:
        cookies = {'sessionid': os.environ['SESSION_ID']}
        await client.login(cookies)
        yield client
