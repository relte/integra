import requests
import os
import json


def send(text, bot_username=None, bot_icon_url=None, bot_icon_emoji=None):
    url = os.getenv('SLACK_WEBHOOK_URL')

    payload = {
        'text': text
    }

    if bot_username:
        payload['username'] = bot_username

    if bot_icon_url:
        payload['icon_url'] = bot_icon_url

    if bot_icon_emoji:
        payload['icon_emoji'] = bot_icon_emoji

    data = {
        'payload': json.dumps(payload)
    }

    requests.post(url=url, data=data)
