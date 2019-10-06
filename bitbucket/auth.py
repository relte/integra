import requests
import os
from base64 import b64encode

from bitbucket import store


def prepare_token():
    token_url = 'https://bitbucket.org/site/oauth2/access_token'

    credentials = os.getenv('BITBUCKET_ACCESS_KEY') + ':' + os.getenv('BITBUCKET_SECRET_KEY')
    headers = {'Authorization': 'Basic ' + b64encode(credentials.encode()).decode()}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url=token_url, headers=headers, data=data)
    response_json = response.json()

    store.save_access_token(response_json['access_token'])


def prepare_account_id():
    user_url = 'https://bitbucket.org/api/2.0/users/%s' % os.getenv('BITBUCKET_USER')

    headers = {'Authorization': 'Bearer ' + store.get_access_token()}

    response = requests.get(url=user_url, headers=headers)
    response_json = response.json()

    store.save_account_id(response_json['account_id'])
