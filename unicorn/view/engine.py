import logging
import asyncio

from unicorn.view.youtube import get_views as youtube_views
from unicorn.view.analytics import get_views as analytics_views
from unicorn.util.config import youtube_config, analytics_config
from unicorn.visualizer.visualizer import Visualizer

logger = logging.getLogger()
analytics = {}
visualizer = Visualizer()

REFRESH_ANALYTICS_SECONDS = 300
TIME_SCALE_SECONDS = 900
FRAME_TIME = 0.08


async def start(options):
    startup = 'playing events over {}s, updating every {}s, frame time {}s.'
    startup = startup.format(TIME_SCALE_SECONDS, REFRESH_ANALYTICS_SECONDS, FRAME_TIME)
    logging.info(startup)

    loop = asyncio.get_event_loop()
    loop.create_task(update(options))
    loop.create_task(render())


async def update_youtube():
    for view in youtube_config()['channels']:
        views = await youtube_views(view['channel'])
        analytics[view['name']] = create_data(view, views)


async def update_analytics():
    for view in analytics_config()['views']:
        views = await analytics_views(view['id'])
        analytics[view['name']] = create_data(view, views)


async def update(options):
    """ updates the analytics data using google APIs. """
    while True:
        logging.info('updating statistics from Google API..')

        if options.youtube:
            await update_youtube()

        if options.analytics:
            await update_analytics()

        logging.info('next update in {}s.'.format(REFRESH_ANALYTICS_SECONDS))
        await asyncio.sleep(REFRESH_ANALYTICS_SECONDS)


def create_data(view, views):
    logging.info('update ' + str(views) + ' views @ ' + view['name'])
    return {
        'views': int(views),
        'color': view['color'],
        'delta': 0.0
    }


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


def close():
    visualizer.close()
