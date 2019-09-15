import requests
import os
import hashlib
import json
from datetime import datetime

import store


def pull_requests_to_review(repository):
    url = 'https://bitbucket.org/api/2.0/repositories/%s/pullrequests' % repository

    parameters = {
        'q': 'state = "OPEN" AND reviewers.nickname = "%s"' % os.getenv('BITBUCKET_USER'),
        'pagelen': 20
    }

    headers = {'Authorization': 'Bearer ' + store.get_access_token()}

    print('\nFetching pull requests for %s at %s' % (repository, datetime.now().strftime("%d.%m.%Y %H:%M")))
    response = requests.get(url=url, headers=headers, params=parameters)
    response_json = response.json()

    pull_requests = []
    for value in response_json['values']:
        if not checked_before(value):
            pull_requests.append({
                'title': value['title'],
                'href': value['links']['html']['href']
            })
            store.save_pull_request(str(value['id']), generate_pull_request_hash(value))
            print('"%s" is new or has been updated' % value['title'])

    if len(pull_requests) == 0:
        print('No updates')

    return pull_requests


def checked_before(pull_request):
    saved_pull_requests = store.get_pull_requests()
    for saved_pull_request_id, saved_pull_request in saved_pull_requests.items():
        pull_request_hash = generate_pull_request_hash(pull_request)

        if str(pull_request['id']) == saved_pull_request_id and pull_request_hash == saved_pull_request:
            return True

    return False


def generate_pull_request_hash(pull_request):
    return hashlib.sha512(json.dumps(pull_request).encode()).hexdigest()
