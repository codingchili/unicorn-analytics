import asyncio
import time

from .youtube_views import get_views as youtube_views
from .analytics_views import get_views as analytics_views
from .config import youtube_config, analytics_config
from .api_call import on_loop
from .visualizer import Visualizer

TIME_SCALE_SECONDS = 300
FRAME_TIME = 0.08

analytics = {}
visualizer = Visualizer()

async def update():
    """ updates the analytics data using google APIs. """
    while True:
        views = await youtube_views(youtube_config()['channel'])
        analytics['youtube'] = {
            'views': int(views),
            'color': youtube_config()['color'],
            'delta': 0.0
        }

        for view in analytics_config()['views']:
            views = await analytics_views(view['id']) 
            analytics[view['name']] = {
                'views': int(views),
                'color': view['color'],
                'delta': 0.0
            }

        await asyncio.sleep(30)


async def render():
    """ renders the analytics data onto the unicorn hat. """
    while True:
        for name in analytics:
            stats = analytics[name]
            stats['delta'] += FRAME_TIME * (stats['views'] / TIME_SCALE_SECONDS)

            while stats['delta'] > 1:
                stats['delta'] -= 1
                visualizer.add_python(stats['color'])
        
        visualizer.render()
        await asyncio.sleep(FRAME_TIME)


loop = asyncio.get_event_loop()

# set the event loop for the HTTP client.
on_loop(loop)

try:
    loop.create_task(update())
    loop.create_task(render())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    visualizer.close()
    loop.close()
