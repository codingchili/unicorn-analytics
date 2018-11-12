import json


def load_json(file):
    with open(file) as config:
        return json.load(config)


def youtube_config():
    return load_json('config/youtube.json')


def analytics_config():
    return load_json('config/analytics.json')