import requests
import os
import json


def send(text):
    url = os.getenv('SLACK_WEBHOOK_URL')

    payload = {
        'text': text
    }

    data = {
        'payload': json.dumps(payload)
    }

    requests.post(url=url, data=data)
