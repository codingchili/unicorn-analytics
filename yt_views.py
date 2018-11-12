import requests

yt_url = 'https://content-youtubeanalytics.googleapis.com/v2/reports'
yt_params = {
    'startDate': '2000-01-01',
    'endDate': '2020-01-01',
    'ids': 'channel==MINE',
    'metrics': 'views',
    'sort': '-views'
}
yt_headers = {
    'x-referer': 'https://developers.google.com/',
    'authorization': 'NFYE'
}


def get_views():
    response = requests.get(yt_url, headers=yt_headers, params=yt_params)
    print(response)
    views = response.json()['rows'][0][0]
    print('current views for channel: ' + str(views))
    return views


get_views()