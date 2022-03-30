import asyncio
import logging
import argparse
import json
import re

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

file = open('shipper/config.json', 'r')
config = json.load(file)
file.close()

# note this is not perfect for the 172.16.x.x private range.
private_pattern = re.compile('(192\\.168.*)|(10\\..*)|(172\\.[1-3]+.*)')


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


def private_ip(ip):
    global private_pattern
    return private_pattern.match(ip)


def color_proto(proto, app):
    global config
    applications = config['applications']
    protocols = config['protocols']

    if app in applications:
        return applications[app]["color"]
    elif proto in protocols:
        return protocols[proto]["color"]
    return config["default"]["color"]


def length(event):
    if 'flow' in event:
        packets = event['flow']['pkts_toserver'] + event['flow']['pkts_toclient']
        # one per 100 packets, plus one.
        return int(packets / 100) + 1
    elif 'fileinfo' in event:
        # one per 10KB, plus one.
        return int(event["fileinfo"]["size"] / 10_000) + 1
    else:
        return 1


async def process(line):
    global events
    try:
        event = json.loads(line)
        event_type = event["event_type"]
        request = {}

        if event_type in ['flow', 'fileinfo', 'tls']:
            request["length"] = min(length(event), 10)
            request["direction"] = 'up' if private_ip(event["src_ip"]) else 'down'
            request["color"] = color_proto(event['proto'], event.get('app_proto', event_type))
            request["reason"] = f"eve-[{event['proto']}]-[{event.get('app_proto', event_type)}]"
            request["token"] = args.token
            events += 1
            await write(request)
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
