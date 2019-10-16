import re

from app import locators


LOCATOR_GROUPS = {
    locators.OPEN_QUEUE: ['ID', 'client_email'],
    locators.SERVER_NOTICE_QUEUE: ['ID'],
    locators.SEND_ATTEMPT: ['ID', 'receiver_email', 'status'],
    locators.CLOSE_QUEUE: ['ID'],
}


class ParseLogLine:
    def __init__(self, line):
        self.line = line

    def parser(self, locator):
        found = re.search(locator, self.line)
        if found:
            return zip(LOCATOR_GROUPS[locator], found.groups())