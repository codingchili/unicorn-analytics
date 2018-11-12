import asyncio

from .youtube_views import get_views as youtube_views
from .analytics_views import get_views as analytics_views
from .config import youtube_config, analytics_config
from .api_call import on_loop


async def update():
    """ sample main. """
    while True:
        print(await youtube_views(youtube_config()['channel']))

        for view in analytics_config()['views']:
            print(view['name'] + ": #" + await analytics_views(view['id']))

        print("wait for 5 until update.")
        await asyncio.sleep(5)


async def render():
    while True:
        print('hat update for 1s.')
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()

# set the event loop for the HTTP client.
on_loop(loop)

try:
    loop.create_task(update())
    loop.create_task(render())
    loop.run_forever()
finally:
    loop.close()
