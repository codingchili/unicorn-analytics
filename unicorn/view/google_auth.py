from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
import argparse
import os.path
import httplib2
import socket

API_YOUTUBE = 'youtube'
API_ANALYTICS = 'analytics'

SCOPE_YOUTUBE = 'https://www.googleapis.com/auth/youtube.readonly ' \
                'https://www.googleapis.com/auth/yt-analytics.readonly ' \
                'https://www.googleapis.com/auth/yt-analytics-monetary.readonly '

SCOPE_ANALYTICS = 'https://www.googleapis.com/auth/analytics ' \
                  'https://www.googleapis.com/auth/analytics.readonly'


class Flags:
    pass


def authenticate(api_name):
    """ authenticates using OAUTH2 with the given API. """
    if not os.path.isfile(credentials_file(api_name)):
        # if there is no credentials: run the flow.
        flow = flow_from_clientsecrets(secret_file(api_name),
                                   scope=get_scope(api_name))

        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()

        # override default port with a random free port to avoid issues when
        # a second flow is initiated using the same port.
        override = Flags()
        # convert argparse.Namespace to dict to make it writable.
        override.__dict__ = flags.__dict__
        # make sure we have a unique port.
        override.auth_host_port = [free_port()]
        # avoid having logging disabled.
        override.logging_level = 'INFO'

        storage = Storage(credentials_file(api_name))
        tools.run_flow(flow, storage, flags)

    token = Storage(credentials_file(api_name)).get()

    if token.access_token_expired:
        token.refresh(httplib2.Http())

    return token.access_token


def free_port():
    """ grab a free TCP port, we can't use 0 as the oauth2 library grabs the port from the URL."""
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def get_scope(api):
    """ returns the credentials scope required for interacting with the given API. """
    if api == API_YOUTUBE:
        return SCOPE_YOUTUBE
    elif api == API_ANALYTICS:
        return SCOPE_ANALYTICS
    else:
        raise ValueError("Unknown API " + api + ", use " + API_ANALYTICS + " or " + API_YOUTUBE)


def credentials_file(api_name):
    """ returns a path to the file where credentials are to be stored. """
    return 'api_keys/' + api_name + '_credentials.json'


def secret_file(api_name):
    """ returns a path to the file where the client secret is stored. """
    return 'api_keys/' + api_name + '_secret.json'
