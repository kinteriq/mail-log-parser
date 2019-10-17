import re

from app import locators


class ParseLogLine:
    def __init__(self, line):
        self.line = line

    def parser(self, locator):
        found = re.search(locator, self.line)
        if found:
            return zip(locators.GROUPS[locator], found.groups())