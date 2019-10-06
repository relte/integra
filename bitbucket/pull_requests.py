import requests
import os
import hashlib
import json
from datetime import datetime

from bitbucket import store


def pull_requests_to_review(repository):
    url = 'https://bitbucket.org/api/2.0/repositories/%s/pullrequests' % repository

    parameters = {
        'q': 'state = "OPEN" AND reviewers.account_id = "%s"' % store.get_account_id(),
        'pagelen': 20
    }

    headers = {'Authorization': 'Bearer ' + store.get_access_token()}

    print('\nFetching pull requests for %s at %s' % (repository, datetime.now().strftime("%d.%m.%Y %H:%M")))
    response = requests.get(url=url, headers=headers, params=parameters)
    response_json = response.json()

    pull_requests = []
    for value in response_json['values']:
        if not checked_before_or_same(value):
            pull_requests.append({
                'title': value['title'],
                'href': value['links']['html']['href']
            })
            store.save_pull_request(str(value['id']), generate_hash(value))
            print('"%s" is new or has been updated' % value['title'])

    if len(pull_requests) == 0:
        print('No updates')

    return pull_requests


def own_pull_requests(repository):
    user = os.getenv('BITBUCKET_USER')
    url = 'https://bitbucket.org/api/2.0/pullrequests/%s' % user

    headers = {'Authorization': 'Bearer ' + store.get_access_token()}

    print('\nFetching %s\'s pull requests for %s at %s' % (user, repository, datetime.now().strftime("%d.%m.%Y %H:%M")))
    response = requests.get(url=url, headers=headers)
    response_json = response.json()
    pull_requests = response_json['values']

    result = []
    for pull_request in pull_requests:
        destination_repository = pull_request['destination']['repository']['full_name']
        source_repository = pull_request['source']['repository']['full_name']
        if repository != destination_repository or destination_repository != source_repository:
            continue

        own_pull_request_activity = __own_pull_request_activity(repository, pull_request['id'])
        activity_hash = generate_hash(own_pull_request_activity)

        if not own_checked_before_or_same(pull_request['id'], activity_hash):
            result.append({
                'title': pull_request['title'],
                'href': pull_request['links']['html']['href']
            })
            store.save_own_pull_request(pull_request['id'], activity_hash)
            print('Something new happened at your PR "%s"' % pull_request['title'])

    if len(result) == 0:
        print('No updates')

    return result


def __own_pull_request_activity(repository, pull_request_id):
    url = 'https://bitbucket.org/api/2.0/repositories/%s/pullrequests/%s/activity' % (repository, pull_request_id)

    headers = {'Authorization': 'Bearer ' + store.get_access_token()}

    response = requests.get(url=url, headers=headers)
    response_json = response.json()
    activities = response_json['values']
    change_by_others = list(filter(lambda activity: 'update' not in activity, activities))

    return change_by_others


def checked_before_or_same(pull_request):
    saved_pull_requests = store.get_pull_requests()
    for saved_pull_request_id, saved_pull_request in saved_pull_requests.items():
        pull_request_hash = generate_hash(pull_request)

        if str(pull_request['id']) == saved_pull_request_id and pull_request_hash == saved_pull_request:
            return True

    return False


def own_checked_before_or_same(pull_request_id, activity_hash):
    saved_pull_requests = store.get_own_pull_requests()
    for saved_pull_request_id, saved_pull_request in saved_pull_requests.items():
        if str(pull_request_id) == saved_pull_request_id and activity_hash == saved_pull_request:
            return True

    return False


def generate_hash(payload):
    return hashlib.sha512(json.dumps(payload).encode()).hexdigest()
