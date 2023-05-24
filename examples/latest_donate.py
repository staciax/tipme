# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

import asyncio

from tipme import TipMeClient


async def main():
    cookies = {'sessionid': 'get your session id from https://tipme.in.th'}  # use browser to get session id
    async with TipMeClient() as client:
        await client.login(cookies)
        donates = await client.fetch_latest_donates()
        print(donates)


if __name__ == '__main__':
    asyncio.run(main())
