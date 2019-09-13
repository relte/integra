import requests
import os

import store


def pull_requests_to_review(repository):
    url = 'https://bitbucket.org/api/2.0/repositories/%s/pullrequests' % repository

    parameters = {
        'q': 'state = "OPEN" AND reviewers.nickname = "%s"' % os.getenv('BITBUCKET_USER'),
        'pagelen': 20
    }

    headers = {'Authorization': 'Bearer ' + store.get_access_token()}

    response = requests.get(url=url, headers=headers, params=parameters)
    response_json = response.json()

    pull_requests = []
    for value in response_json['values']:
        pull_requests.append({
            'title': value['title'],
            'href': value['links']['html']['href']
        })

    return pull_requests
