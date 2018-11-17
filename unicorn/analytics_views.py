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
    """ retrieves the number of page loads for the given view ID. """

    params['ids'] = view_id
    params['start-date'] = week()
    params['end-date'] = today()
    headers['authorization'] = 'Bearer ' + authenticate(API_ANALYTICS)

    views = 0
    response = await get(url, headers, params)

    if (len(response['rows']) > 0 and len(response['rows'][0]) > 0):
        views = response['rows'][0][0]

    return views
