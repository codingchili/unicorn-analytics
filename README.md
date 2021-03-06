# unicorn-analytics
Unicorn analytics retrieves analytics data from the **YouTube Analytics API** and **Google Analytics API**.
The unicorn in the story is the [unicorn hat HD](https://shop.pimoroni.com/products/unicorn-hat-hd). Page hits
and video views are visualized as a snake crawling over the unicorn display. One snake equals one page load or view.

If you don't have that many views you can set a scaling factor - for example we can retrieve the statistics
over the last week; and display them over 5 minutes - then refresh the statistics and play them again for 5 minutes.

![sample image from internet](https://thumbs.gfycat.com/ConventionalFrightenedBorzoi-size_restricted.gif)

GIF of me running the unicorn-analytics on a Raspberry PI 3, replaying page loads and youtube views for the last week over 5 minutes. I used the configuration that is checked in here: [unicorn-analytics/config](https://github.com/codingchili/unicorn-analytics/tree/master/config)

Related project: [pi-zero-ethermeter](https://github.com/codingchili/pi-zero-ethermeter)

# Setup
You need at least one raspberry pi with a unicorn HAT. 
The raspberry pi needs python 3.5+ to support await/async.

Modules that **needs** to be installed,

```console
pip3 install oauth2client aiohttp
pip3 install unicornhathd numpy
```

- aiohttp: to asynchronously update the statistics without disturbing the animations.
- oauth2client: used to retrieve oauth2 tokens from gooooogle.
- httplib2: to update the access token when it expires its a bit messy so we didn't implement this with aiohttp.

Now is a good time to **configure your google APIs**, see the section on **Configuration**.

To start it all up run,
```console
git clone https://github.com/codingchili/unicorn-analytics
cd unicorn-analytics
python -m unicorn.run
```

Make sure you have configured everything first :smirk:

The first time it is launched it will ask you to open your browser and allow third party access.
If you don't have a browser available on your PI, please run as follows:
```
python -m unicorn.run --noauth_local_webserver
```

And open your browser on another machine.

# Supported API's

- Google Analytics
- YouTube Analytics

### Configuration
Perform the following and update `config/analytics.json` and `config/youtube.json`

- create a new Google Analytics project, grab the view ID.
- make sure there is a YouTube channel registered on your Google account.

Create a new API project on the google developers console
- [developers console](https://console.developers.google.com/)
- enable "YouTube Analytics API"
- enable "Analytics API"

Create an OAUTH2 client secret by following these instructions;
- https://developers.google.com/identity/protocols/OAuth2

Download it as json and place under `api_keys/analytics_secret.json` and `api_keys/youtube_secret.json`.

# Additional notes

For the youtube analytics API we may **only** authenticate using a OAUTH2 token. Most of the examples in the docs assume 
that we are a web application. Some hours later I actually found out that there IS a flow that can be used from the 
commandline! Scroll to the bottom of the following page:

https://developers.google.com/api-client-library/python/guide/aaa_oauth#the-oauth2client-library

With this we can actually generate oauth2 tokens without requiring a browser to be opened on the PI. If you 
don't have a browser available in your environment please pass the commandline parameter

```console
--noauth_local_webserver
```

# Contributing
All contributions welcome. :fish: :sweat_drops:
