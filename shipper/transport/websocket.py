import asyncio

import aiohttp

connected = False
connecting = False
websocket = None


async def ws_connect(server):
    global websocket, connecting, connected

    if connecting:
        await asyncio.sleep(3)
    elif not connected:
        connecting = True
        try:
            session = aiohttp.ClientSession()
            websocket = await session.ws_connect(server)
            connected = True
        finally:
            connecting = False


async def ws_disconnect():
    global websocket, connected
    connected = False

    if websocket is not None:
        try:
            await websocket.close()
        except Exception as e:
            pass


async def write_ws(data, server):
    global websocket
    try:
        await ws_connect(server)
        if connected:
            await websocket.send_json(data)
    except Exception as e:
        await ws_disconnect()
        raise e
