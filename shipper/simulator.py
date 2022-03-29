import asyncio
import json
import random
import logging

from shipper.util.ansi import *

logging.basicConfig(format=f'{magenta("%(asctime)s")} [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
events = [
    {'src_ip': '192.168.0.1', 'proto': 'TCP', 'event_type': 'flow',
     'flow': {'pkts_toclient': 95, 'pkts_toserver': 50}},
    {'src_ip': '172.16.0.1', 'proto': 'UDP', 'event_type': 'flow',
     'flow': {'pkts_toclient': 0, 'pkts_toserver': 0}},
    {'src_ip': '172.31.0.1', 'proto': 'ICMP', 'event_type': 'flow',
     'flow': {'pkts_toclient': 0, 'pkts_toserver': 0}},
    {'src_ip': '10.0.0.1', 'proto': 'IPv6-ICMP', 'event_type': 'flow',
     'flow': {'pkts_toclient': 0, 'pkts_toserver': 0}},
    {'src_ip': '1.1.1.1', 'proto': 'UDP', 'app_proto': 'dhcp', 'event_type': 'flow',
     'flow': {'pkts_toclient': 300, 'pkts_toserver': 45}},
    {'src_ip': '10.0.0.1', 'proto': 'TCP', 'app_proto': 'tls', 'event_type': 'flow',
     'flow': {'pkts_toclient': 0, 'pkts_toserver': 0}},
    {'src_ip': '1.1.1.1', 'proto': 'UDP', 'app_proto': 'dns', 'event_type': 'flow',
     'flow': {'pkts_toclient': 20, 'pkts_toserver': 50}},
    {'src_ip': '1.1.1.1', 'proto': 'TCP', 'app_proto': 'http', 'event_type': 'flow',
     'flow': {'pkts_toclient': 0, 'pkts_toserver': 0}},
]


async def sim():
    global events

    with open('./shipper/tmp/testfile.jsonl', 'a') as file:
        while True:
            await asyncio.sleep(random.randint(1, 4) / 10)
            event = random.choice(events)
            file.write(json.dumps(event) + '\n')
            file.flush()
            logger.info(event)


loop = asyncio.new_event_loop()
loop.run_until_complete(sim())
