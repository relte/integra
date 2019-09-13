import json


def init():
    data = {'access_token': ''}
    __save(data)


def save_access_token(token):
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['access_token'] = token
        __save(data)


def get_access_token():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data['access_token']


def __save(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
