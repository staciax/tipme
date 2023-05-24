from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.


if TYPE_CHECKING:
    from tipme import TipMeClient


@pytest.mark.asyncio
async def test_latest_donates(client: TipMeClient):
    donates = await client.fetch_latest_donates()
    for donate in donates:
        assert donate.author is not None
        assert donate.amount is not None
        assert donate.channel is not None
        assert donate.reference_number is not None
        assert donate.datetime is not None
        if donate.message is not None:
            assert isinstance(donate.message, str)
        assert isinstance(donate.amount, float)
