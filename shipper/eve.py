import asyncio
import logging
import argparse
import json

from shipper.transport.websocket import write_ws
from shipper.transport.rest import write_http
from shipper.util.ansi import *

logging.basicConfig(format=f'{magenta("%(asctime)s")} [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Eve events shipper.')
parser.add_argument('--server', help='url to the server ws:// or http://.')
parser.add_argument('--file', help='the file to tail.')
parser.add_argument('--token', help='token used for authentication.')
args = parser.parse_args()

POLL_INTERVAL = 0.02
events = 0


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


async def process(line):
    global events
    try:
        data = json.loads(line)
        # process, filter etc.
        events += 1
        # data["length"] = 3
        # data["color"] = '#ff00cc'
        # data["direction"] = 'right'
        data["reason"] = "testing the api"
        data["token"] = args.token
        await write(data)
    except Exception as e:
        logger.warning(f"event error: '{yellow(str(e))}'")


async def write(data):
    if 'ws://' in args.server:
        await write_ws(data, args.server)
    elif 'http://' in args.server:
        await write_http(data, args.server)
    else:
        logger.warning(f"{red('unknown')} protocol expected {cyan('ws://')} or {cyan('http://')}.")
        asyncio.get_event_loop().stop()


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
