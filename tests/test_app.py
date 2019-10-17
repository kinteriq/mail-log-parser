import os
import unittest

from .context import mail_log_parser
from mail_log_parser.app import main


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOG = os.path.join(os.getcwd(), 'maillog')
        cls.SHORT_LOG = {
            'path': os.path.join(os.getcwd(), 'maillog_excerpt'),
            'limit': 100,
        }
        with open(cls.SHORT_LOG['path'], 'w') as short_log:
            with open(LOG, 'r') as original:
                for _ in range(cls.SHORT_LOG['limit']):
                    short_log.write(original.readline())

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.SHORT_LOG['path'])

    def test_main(self):
        self.assertIsNone(main(self.SHORT_LOG['path']))


if __name__ == '__main__':
    unittest.main()