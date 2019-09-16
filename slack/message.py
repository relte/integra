from datetime import datetime


class PullRequestMessageBuilder:
    def __init__(self):
        self.message = ''

    def with_current_date(self):
        self.message += '%s\n' % datetime.now().strftime("%d.%m.%Y %H:%M")

    def with_repository(self, name, link):
        self.message += '<%s|*%s*>\n' % (link, name)

    def with_pull_request(self, title, link):
        self.message += ':white_small_square: <%s|%s>\n' % (link, title)

    def with_new_line(self):
        self.message += '\n'

    def build(self):
        return self.message
