import json


def init():
    data = {'access_token': '', 'pull_requests': {}}
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


def save_pull_request(pull_request_id, pull_request_hash):
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['pull_requests'][pull_request_id] = pull_request_hash
        __save(data)


def get_pull_requests():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data['pull_requests']


def __save(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
