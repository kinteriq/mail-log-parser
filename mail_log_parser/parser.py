import re

from .locators import GROUPS


class ParseLogLine:
    def __init__(self, line):
        self.line = line

    def parser(self):
        for locator in GROUPS:
            found = re.search(locator, self.line)
            if found:
                return list(zip(GROUPS[locator], found.groups()))