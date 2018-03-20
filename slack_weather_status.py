#!/usr/bin/env python3

import json

import requests

SLACK_API_KEY = "get token from https://api.slack.com/custom-integrations/legacy-tokens"
OPENWEATHER_API_KEY = "get token from https://openweathermap.org/appid"
OPENWEATHER_CITY_ID = "find your city id https://openweathermap.org/current#cityid"

# https://openweathermap.org/weather-conditions
WEATHER_CODES = {
    '2': ':lightning:',
    '3': ':rain_cloud:',
    '5': ':rain_cloud:',
    '6': ':snowflake:',
    '7': ':fog:',
    '80': ':cloud:',
    '800': ':sunny:',
    '801': ':sun_small_cloud:',
}


def get_emoji(code):
    code = str(code)
    if code in WEATHER_CODES:
        return WEATHER_CODES.get(code)

    if code[:2] in WEATHER_CODES:
        return WEATHER_CODES.get(code[:2])

    if code[:1] in WEATHER_CODES:
        return WEATHER_CODES.get(code[:1])


def to_celsius(kelvin):
    return kelvin - 273.15


def build_status(text, emoji):
    payload = {
        'status_text': text,
        'status_emoji': emoji
    }
    return json.dumps(payload)


if __name__ == '__main__':
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id={}&appid={}'.format(OPENWEATHER_CITY_ID,
                                                                                            OPENWEATHER_API_KEY))

    weather = r.json().get('weather')[0]
    temp = to_celsius(r.json().get('main').get('temp'))

    text = '{}°C and {}'.format(round(temp), weather.get('description'))
    emoji = get_emoji(weather.get('id'))

    r = requests.post('https://slack.com/api/users.profile.set', verify=False, data={
        'token': SLACK_API_KEY,
        'profile': build_status(text, emoji)
    })

    if r.status_code != 200:
        print(r.status_code)
        print(r.json())
