import asyncio
import aiohttp


async def get(url, headers=None, params=None):
    """ issues a POST request for the given url. """
    loop = asyncio.get_event_loop()

    if params is None:
        params = {}
    if headers is None:
        headers = {}

    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status >= 400:
                print(str(response.status) + ": " + await response.text())
            else:
                return await response.json()
