import json


def load_json(file):
    """ loads the given file as a JSON object. """
    with open(file) as config:
        return json.load(config)


def youtube_config():
    """ returns the configuration for youtube. """
    return load_json('config/youtube.json')


def analytics_config():
    """ returns the configuration for google analytics. """
    return load_json('config/analytics.json')
