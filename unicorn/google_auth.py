from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
import argparse
import os.path
import httplib2

API_YOUTUBE = 'youtube'
API_ANALYTICS = 'analytics'

SCOPE_YOUTUBE = 'https://www.googleapis.com/auth/youtube.readonly ' \
                'https://www.googleapis.com/auth/yt-analytics.readonly ' \
                'https://www.googleapis.com/auth/yt-analytics-monetary.readonly '

SCOPE_ANALYTICS = 'https://www.googleapis.com/auth/analytics ' \
                  'https://www.googleapis.com/auth/analytics.readonly'


def authenticate(api_name):
    if not os.path.isfile(credentials_file(api_name)):
        # if there is no credentials: run the flow.
        flow = flow_from_clientsecrets(secret_file(api_name),
                                   scope=get_scope(api_name),
                                   redirect_uri='http://localhost:8080/auth_return')

        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()

        storage = Storage(credentials_file(api_name))
        tools.run_flow(flow, storage, flags)

    token = Storage(credentials_file(api_name)).get()

    if token.access_token_expired:
        token.refresh(httplib2.Http())

    return token.access_token


def get_scope(api):
    if api == API_YOUTUBE:
        return SCOPE_YOUTUBE
    elif api == API_ANALYTICS:
        return SCOPE_ANALYTICS
    else:
        raise ValueError("Unknown API " + api + ", use " + API_ANALYTICS + " or " + API_YOUTUBE)


def credentials_file(api_name):
    return 'api_keys/' + api_name + '_credentials.json'


def secret_file(api_name):
    return 'api_keys/' + api_name + '_secret.json'
