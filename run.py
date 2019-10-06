import os
import sys
import schedule
import time

import bitbucket.auth
import bitbucket.pull_requests
import bitbucket.store
import slack.broadcast
import slack.message


def check():
    bitbucket.auth.prepare_token()
    bitbucket.auth.prepare_account_id()

    message_builder = slack.message.PullRequestMessageBuilder()
    message_builder.with_current_date()
    counter = 0
    for repo in os.getenv('BITBUCKET_REPOSITORIES').split(';'):
        message_builder.with_repository(repo, 'https://bitbucket.org/%s/pull-requests/' % repo)
        pull_requests = bitbucket.pull_requests.pull_requests_to_review(repo)
        own_pull_requests = bitbucket.pull_requests.own_pull_requests(repo)
        counter += len(pull_requests)
        counter += len(own_pull_requests)

        for pull_request in pull_requests:
            message_builder.with_pull_request(pull_request['title'], pull_request['href'])

        for own_pull_request in own_pull_requests:
            message_builder.with_own_pull_request(own_pull_request['title'], own_pull_request['href'])

        message_builder.with_new_line()

    if counter > 0:
        slack.broadcast.send(text=message_builder.build(), bot_username='PR Checker', bot_icon_url='https://cdn4.iconfinder.com/data/icons/web-mobile-dev-1/100/Scheme-512.png')


def schedule_checks(interval):
    schedule.every(int(interval)).seconds.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)


try:
    if sys.argv[1] == 'init':
        bitbucket.store.init()
    else:
        check()
        schedule_checks(sys.argv[1])
except IndexError:
    print('Argument must be provided')
