import os
from datetime import datetime

import auth
import pull_requests
import slack

auth.prepare_token()

repos = os.getenv('BITBUCKET_REPOSITORIES').split(';')
text = ''
text += '%s\n' % datetime.now().strftime("%d.%m.%Y %H:%M")
for repo in repos:
    text += '<%s|*%s*>\n' % ('https://bitbucket.org/%s/pull-requests/' % repo, repo)
    prs = pull_requests.pull_requests_to_review(repo)
    for pr in prs:
        text += ':white_small_square: <%s|%s>\n' % (pr['href'], pr['title'])
    text += '\n'

slack.message(text)
