from .google_auth import authenticate, API_ANALYTICS
from .date_param import today, week
from .api_call import get

url = 'https://www.googleapis.com/analytics/v3/data/ga'

params = {
    'metrics': 'ga:pageviews'
}

headers = {
}


async def get_views(view_id):
    params['ids'] = view_id
    params['start-date'] = week()
    params['end-date'] = today()
    headers['authorization'] = 'Bearer ' + authenticate(API_ANALYTICS)

    return (await get(url, headers, params))['rows'][0][0]
