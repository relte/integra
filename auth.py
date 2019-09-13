import requests
import os
from base64 import b64encode

import store


def prepare_token():
    token_url = 'https://bitbucket.org/site/oauth2/access_token'

    credentials = os.getenv('BITBUCKET_ACCESS_KEY') + ':' + os.getenv('BITBUCKET_SECRET_KEY')
    headers = {'Authorization': 'Basic ' + b64encode(credentials.encode()).decode()}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url=token_url, headers=headers, data=data)
    response_json = response.json()

    store.save_access_token(response_json['access_token'])
