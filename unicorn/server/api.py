import asyncio
import logging
import json
import random
import string

from unicorn.util.config import server_config
from aiohttp import web
from unicorn.util.ansi import *
from unicorn.visualizer.visualizer import Visualizer

config = server_config()
visualizer = Visualizer()
logger = logging.getLogger()
logging.getLogger('asyncio').setLevel(logging.WARNING)

FRAME_TIME = 0.08
TOKEN_LEN = 16


async def start(port):
    runner = web.AppRunner(application(), access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, None, port)
    await site.start()
    logging.info(f"started server on port {blue(port)}.")
    logging.info(f"api available at '{blue('/spawn')}'.")
    logging.info(f"websocket available at '{blue('/websocket')}'.")
    asyncio.get_event_loop().create_task(render())


def application():
    app = web.Application()

    if config['token'] is None:
        config['token'] = random_token()
    else:
        logger.info(f"using token configured in '{blue('server.json')}'.")

    app['token'] = config['token']
    app.add_routes([
        web.post('/spawn', post_handler),
        web.get('/websocket', websocket_handler),
        web.route('*', '/{tail:.*}', any_handler)
    ])
    return app


async def render():
    while True:
        visualizer.render()
        await asyncio.sleep(FRAME_TIME)


async def any_handler(request):
    logger.info(f'{yellow(request.remote)} '
                f'{cyan(request.method)} {blue(request.path)}')
    return web.json_response(response('the server is running.'))


def random_token():
    keyspace = string.ascii_lowercase + string.digits
    token = ''.join([random.choice(keyspace) for _ in range(TOKEN_LEN)])
    logger.info(f"generated random token ({cyan(token)}).")
    return token


async def post_handler(request):
    return web.json_response(process(await request.text()))


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    logger.info(f'websocket connection {green("opened")}.')

    while not ws.closed:
        try:
            await ws.send_json(process(await ws.receive_str()))
        except:
            logger.info(f'websocket connection {red("closed")}.')
            break


def process(data):
    try:
        data = json.loads(data)
        if 'token' in data:
            if data['token'] == config['token']:
                return handle_request(data)
            else:
                message = f"{red('bad')} request token '{red(data['token'])}'."
                return response(message, error=True)
        else:
            message = f"{red('bad')} request, missing token."
            return response(message, error=True)
    except Exception as e:
        return response(f"{red('bad')} request: '{yellow(str(e))}'", error=True)


def response(text='success', error=False):
    if error:
        logger.warning(text)
    return {
        'message': clean(text),
        'error': error
    }


def handle_request(data):
    data['token'] = None

    if {'length', 'color', 'direction'}.issubset(data):
        message = (f"{green('spawning')} --> "
                   f"length={blue(data['length'])} "
                   f"color={blue(data['color'])} "
                   f"direction={blue(data['direction'])}")

        if 'reason' in data:
            message += f" reason='{blue(data['reason'])}'"
        try:
            visualizer.add_python(data['color'], data['length'], data['direction'])
            logger.info(message)
            return response(message)
        except Exception as e:
            return response(f"{red('error')} spawning: '{yellow(str(e))}'.", True)
    else:
        return response(f"spawn method {red('requires')} length, color and direction.", True)
