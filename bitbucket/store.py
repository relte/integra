import json

FILE = 'bitbucket/data.json'


def init():
    data = {'access_token': '', 'account_id': '', 'pull_requests': {}, 'own_pull_requests': {}}
    __save(data)


def save_access_token(token):
    with open(FILE) as json_file:
        data = json.load(json_file)
        data['access_token'] = token
        __save(data)


def get_access_token():
    with open(FILE) as json_file:
        data = json.load(json_file)
        return data['access_token']


def save_account_id(account_id):
    with open(FILE) as json_file:
        data = json.load(json_file)
        data['account_id'] = account_id
        __save(data)


def get_account_id():
    with open(FILE) as json_file:
        data = json.load(json_file)
        return data['account_id']


def save_pull_request(pull_request_id, pull_request_hash):
    with open(FILE) as json_file:
        data = json.load(json_file)
        data['pull_requests'][pull_request_id] = pull_request_hash
        __save(data)


def get_pull_requests():
    with open(FILE) as json_file:
        data = json.load(json_file)
        return data['pull_requests']


def save_own_pull_request(pull_request_id, pull_request_activity_hash=''):
    with open(FILE) as json_file:
        data = json.load(json_file)
        data['own_pull_requests'][pull_request_id] = pull_request_activity_hash
        __save(data)


def get_own_pull_requests():
    with open(FILE) as json_file:
        data = json.load(json_file)
        return data['own_pull_requests']


def __save(data):
    with open(FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)
