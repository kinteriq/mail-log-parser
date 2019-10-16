import os
import unittest

from .context import app
from app.app import read_log_line


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOG_FILE = os.path.join(os.getcwd(), 'maillog')
        cls.SHORTENED_LOG_FILE = os.path.join(os.getcwd(), 'shortened_maillog')
            
        with open(cls.SHORTENED_LOG_FILE, 'w') as log:
            with open(LOG_FILE, 'r') as original:
                for _ in range(100):
                    log.write(original.readline())

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.SHORTENED_LOG_FILE)

    def test_read_log_line(self):
        log_line = read_log_line(self.SHORTENED_LOG_FILE)
        for _ in range(100):
            self.assertIsNotNone(next(log_line))
        with self.assertRaises(StopIteration):
            next(log_line)


if __name__ == '__main__':
    unittest.main()