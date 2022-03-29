from unicorn.view.google_auth import authenticate, API_YOUTUBE
from unicorn.util.date_param import today, week
from unicorn.view.api_call import get

url = 'https://content-youtubeanalytics.googleapis.com/v2/reports'
params = {
    'ids': 'channel==MINE',
    'metrics': 'views',
    'sort': '-views'
}

headers = {
}


async def get_views(channel):
    """ retrieve the amount of views for the given channel ID. """

    params['ids'] = 'channel==' + channel
    params['startDate'] = week()
    params['endDate'] = today()

    headers['authorization'] = 'Bearer ' + authenticate(API_YOUTUBE)

    views = 0
    response = await get(url, headers, params)
    
    if len(response['rows']) > 0 and len(response['rows'][0]) > 0:
        views = response['rows'][0][0]

    return views
