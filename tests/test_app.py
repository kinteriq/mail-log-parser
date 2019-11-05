import os
import unittest
from unittest import mock

from .context import mail_log_parser
from mail_log_parser.app import main, receive_log_file_path


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LOG = os.path.join(os.getcwd(), os.path.join('tests', 'maillog'))
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
        with mock.patch('mail_log_parser.app.receive_log_file_path',
                        lambda: self.SHORT_LOG['path']):
            self.assertIsNone(main())

    def test_no_log_file_path_is_provided(self):
        with self.assertRaises(SystemExit) as e:
            main()
            
    def test_receive_log_file_path_as_sys_argv(self):
        with mock.patch('sys.argv',
            ['mail_log_parser',
             self.SHORT_LOG['path']]
        ):
            self.assertEqual(receive_log_file_path(), self.SHORT_LOG['path'])
        
    def test_receive_wrong_log_file_path(self):
        with self.assertRaises(SystemExit) as e:
            with mock.patch('sys.argv',
                ['mail_log_parser',
                'wrong_filepath_test_mail_log_parser']
            ):
                receive_log_file_path()


if __name__ == '__main__':
    unittest.main()