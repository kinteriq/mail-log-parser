import unittest

from .context import app
from app.parser import ParseLogLine, LOCATOR_GROUPS
from app import locators


class TestParser(unittest.TestCase):
    def setUp(self):
        self.line_open_queue = 'Jul 10 10:09:08 srv24-s-st '\
                              'postfix/qmgr[3043]: 25E6CDF04F4: '\
                              'from=<krasteplokomplekt@yandex.ru>, '\
                              'size=617951, nrcpt=1 (queue active)'
        self.line_server_queue = 'Jul 10 10:09:21 srv24-s-st postfix/qmgr[3043]: D69F5DF04F4: from=<>, size=3104, nrcpt=1 (queue active)'

    def test_parser_open_queue_success(self):
        parse_log_line = ParseLogLine(self.line_open_queue)
        self.assertEqual(
            list(parse_log_line.parser(locators.OPEN_QUEUE)),
            [('ID', '25E6CDF04F4'), ('client_email', 'krasteplokomplekt@yandex.ru')]
        )
    
    def test_parser_server_queue_success(self):
        parse_log_line = ParseLogLine(self.line_server_queue)
        self.assertEqual(
            list(parse_log_line.parser(locators.SERVER_NOTICE_QUEUE)),
            [('ID', 'D69F5DF04F4'), ('client_email', '')]
        )

    def test_parser_sent_attempt_sent(self):
        self.assertTrue('')


if __name__ == '__main__':
    unittest.main()