from .google_auth import authenticate, API_YOUTUBE
from .date_param import today, week
from .api_call import get

url = 'https://content-youtubeanalytics.googleapis.com/v2/reports'
params = {
    'ids': 'channel==MINE',
    'metrics': 'views',
    'sort': '-views'
}

headers = {
}


async def get_views(channel):
    params['ids'] = 'channel==' + channel
    params['startDate'] = week()
    params['endDate'] = today()

    headers['authorization'] = 'Bearer ' + authenticate(API_YOUTUBE)

    return (await get(url, headers, params))['rows'][0][0]
