import asyncio
import logging
import argparse

from unicorn.util.ansi import *
from unicorn.view.engine import close as close_views, start as start_views
from unicorn.server.api import start as start_server

parser = argparse.ArgumentParser(description='Unicorn Analytics.')
parser.add_argument('--server', help='enable the blinkt api server.', action='store_const', const=True)
parser.add_argument('--youtube', help='enable the youtube analytics view.', action='store_const', const=True)
parser.add_argument('--analytics', help='enable the google analytics view.', action='store_const', const=True)
parser.add_argument('--port', help='port to use when server is enabled. (9990)', nargs='?', const=1, default=9990)

logging.basicConfig(format=f'{magenta("%(asctime)s")} [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger()
args = parser.parse_args()

loop = asyncio.new_event_loop()
try:
    if args.server and (args.youtube or args.analytics):
        logger.info("cannot enable both the api server and views.")

    if args.youtube or args.analytics:
        loop.create_task(start_views(args))
        loop.run_forever()
    elif args.server:
        loop.create_task(start_server(args.port))
        loop.run_forever()
    else:
        logger.info('specify either server mode (--server) or view mode (--youtube, --analytics).')
except KeyboardInterrupt:
    pass
finally:
    close_views()
   # loop.close()
