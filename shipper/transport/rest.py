import aiohttp


async def write_http(data, server):
    async with aiohttp.ClientSession() as session:
        async with session.post(server, json=data):
            pass
