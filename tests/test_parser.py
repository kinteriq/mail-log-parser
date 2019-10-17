import unittest

from .context import app
from app.parser import ParseLogLine
from app import locators


class MockLines:
    LINE_OPEN_QUEUE = (
        'Jul 10 10:09:08 srv24-s-st postfix/qmgr[3043]: '
        '25E6CDF04F4: from=<krasteplokomplekt@yandex.ru>, '
        'size=617951, nrcpt=1 (queue active)'
    )
    LINE_SERVER_QUEUE = (
        'Jul 10 10:09:21 srv24-s-st postfix/qmgr[3043]: '
        'D69F5DF04F4: from=<>, size=3104, nrcpt=1 (queue active)'
    )
    LINE_SEND_ATTEMPT_SUCCESS = (
        'Jul 10 10:09:09 srv24-s-st postfix/smtp[22621]: '
        '25E6CDF04F4: to=<arsenal-krsk@mail.ru>, '
        'relay=mxs.mail.ru[94.100.176.20]:25, delay=33, '
        'delays=32/0/0.01/0.76, dsn=2.0.0, status=sent '
        '(250 OK id=1SoTcj-0001fx-Bs)'
    )
    LINE_SEND_ATTEMPT_FAIL = (
        'Jul 10 10:09:21 srv24-s-st postfix/smtp[6782]: '
        '718F4DF04E9: to=<arsenya08@mail.ru>, '
        'relay=mxs.mail.ru[94.100.176.20]:25, delay=21, '
        'delays=21/0/0.02/0.14, dsn=5.0.0, status=bounced '
        '(host mxs.mail.ru[94.100.176.20] said: 550 Message '
        'was not accepted -- invalid mailbox.  Local '
        'mailbox arsenya08@mail.ru is unavailable: '
        'user not found (in reply to end of DATA command))'
    )
    LINE_CLOSE_QUEUE = (
        'Jul 10 10:09:20 srv24-s-st postfix/qmgr[3043]: '
        'F1DB8DF04EF: removed'
    )


class TestParser(unittest.TestCase):
    def test_parser_open_queue_success(self):
        parse_log_line = ParseLogLine(MockLines.LINE_OPEN_QUEUE)
        self.assertEqual(
            list(parse_log_line.parser(locators.OPEN_QUEUE)),
            [('ID', '25E6CDF04F4'),
            ('client_email', 'krasteplokomplekt@yandex.ru')]
        )
    
    def test_parser_server_queue_success(self):
        parse_log_line = ParseLogLine(MockLines.LINE_SERVER_QUEUE)
        self.assertEqual(
            list(parse_log_line.parser(locators.SERVER_NOTICE_QUEUE)),
            [('ID', 'D69F5DF04F4'), ('client_email', '')]
        )

    def test_parser_sent_attempt_sent(self):
        parse_log_line = ParseLogLine(MockLines.LINE_SEND_ATTEMPT_SUCCESS)
        self.assertEqual(
            list(parse_log_line.parser(locators.SEND_ATTEMPT)),
            [('ID', '25E6CDF04F4'),
            ('receivers', 'arsenal-krsk@mail.ru'),
            ('status', 'sent')]
        )
    
    def test_parser_sent_attempt_not_sent(self):
        parse_log_line = ParseLogLine(MockLines.LINE_SEND_ATTEMPT_FAIL)
        self.assertEqual(
            list(parse_log_line.parser(locators.SEND_ATTEMPT)),
            [('ID', '718F4DF04E9'),
            ('receivers', 'arsenya08@mail.ru'),
            ('status', 'bounced')]
        )
    
    def test_parser_close_queue(self):
        parse_log_line = ParseLogLine(MockLines.LINE_CLOSE_QUEUE)
        self.assertEqual(
            list(parse_log_line.parser(locators.CLOSE_QUEUE)),
            [('ID', 'F1DB8DF04EF')]
        )


if __name__ == '__main__':
    unittest.main()