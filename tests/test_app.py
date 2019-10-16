import os
import unittest

from .context import app
from app.app import read_log_line


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOG = os.path.join(os.getcwd(), 'tests', 'maillog')
        cls.SHORT_LOG = {
            'path': os.path.join(os.getcwd(), 'shortened_maillog'),
            'limit': 100,
        }
        with open(cls.SHORT_LOG['path'], 'w') as short_log:
            with open(LOG, 'r') as original:
                for _ in range(cls.SHORT_LOG['limit']):
                    short_log.write(original.readline())

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.SHORT_LOG['path'])

    def test_read_log_line(self):
        log_line = read_log_line(self.SHORT_LOG['path'])
        for _ in range(self.SHORT_LOG['limit']):
            self.assertIsNotNone(next(log_line))
        with self.assertRaises(StopIteration):
            next(log_line)


if __name__ == '__main__':
    unittest.main()