import os

import bitbucket.auth
import bitbucket.pull_requests
import slack.broadcast
import slack.message

bitbucket.auth.prepare_token()

message_builder = slack.message.PullRequestMessageBuilder()
message_builder.with_current_date()
counter = 0
for repo in os.getenv('BITBUCKET_REPOSITORIES').split(';'):
    message_builder.with_repository(repo, 'https://bitbucket.org/%s/pull-requests/' % repo)
    pull_requests = bitbucket.pull_requests.pull_requests_to_review(repo)
    counter += len(pull_requests)
    for pull_request in pull_requests:
        message_builder.with_pull_request(pull_request['title'], pull_request['href'])
    message_builder.with_new_line()

if counter > 0:
    slack.broadcast.send(message_builder.build())
