import asyncio
import aiohttp
import logging
import argparse
import json

from shipper.util.ansi import *

logging.basicConfig(format=f'{magenta("%(asctime)s")} [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Eve events shipper.')
parser.add_argument('--server', help='url to the server ws:// or http://.')
parser.add_argument('--file', help='the file to tail.')
parser.add_argument('--token', help='token used for authentication.')
args = parser.parse_args()

websocket = None
events = 0

POLL_INTERVAL = 0.02


async def write_http(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(args.server, json=data) as response:
            await response.text()


async def write_ws(data):
    global websocket

    if websocket is None or websocket.closed:
        session = aiohttp.ClientSession()
        websocket = await session.ws_connect(args.server)

    await websocket.send_json(data)


async def post(data):
    if 'ws://' in args.server:
        await write_ws(data)
    elif 'http://' in args.server:
        await write_http(data)
    else:
        logger.warning(f"{red('unknown')} protocol expected {cyan('ws://')} or {cyan('http://')}.")
        asyncio.get_event_loop().stop()


async def process(line):
    global events
    try:
        data = json.loads(line)
        # process, filter etc.
        events += 1
        #data["length"] = 3
        #data["color"] = '#ff00cc'
        #data["direction"] = 'right'
        data["reason"] = "testing the api"
        data["token"] = args.token
        await post(data)
    except Exception as e:
        logger.warning(f"event error: '{yellow(str(e))}'")


async def reader():
    try:
        file = open(args.file, 'a+')
        logger.info(f"tailing file '{blue(args.file)}' ..")
    except Exception as e:
        logger.error(str(e))
        asyncio.get_event_loop().stop()
        return

    while True:
        line = file.readline()
        if not line or not line.endswith('\n'):
            await asyncio.sleep(POLL_INTERVAL)
            continue
        else:
            line = line[:-1]
            loop.create_task(process(line))


async def stats():
    while True:
        logger.info(f"waiting for events [events = {blue(events)}]")
        await asyncio.sleep(0.5)


loop = asyncio.new_event_loop()
try:
    if args.file and args.server and args.token:
        logger.info(f"forwarding events to server '{blue(args.server)}'.")
        loop.create_task(reader())
        loop.create_task(stats())
        loop.run_forever()
    else:
        logger.error(f"all of --file, --server and --token are {red('required')} arguments.")
except KeyboardInterrupt:
    logger.info('shutting down')
    pass
