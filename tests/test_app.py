import os
import unittest
from unittest import mock

from .context import mail_log_parser
from mail_log_parser.app import main, receive_log_file_path


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database_path = os.path.join(os.getcwd(), 'test_results.db')
        cls.short_log = {
            'path': os.path.join(os.getcwd(), 'maillog_excerpt'),
            'limit': 100,
        }
        with open(cls.short_log['path'], 'w') as short_log:
            with open(os.path.join(os.getcwd(),
                                   os.path.join('tests', 'maillog')),
                'r') as original:
                for _ in range(cls.short_log['limit']):
                    short_log.write(original.readline())

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.short_log['path'])
        if os.path.exists(cls.database_path):
            os.remove(cls.database_path)

    def test_main(self):
        with mock.patch('mail_log_parser.app.receive_log_file_path',
                        lambda: self.short_log['path']):
            self.assertIsNone(main(self.database_path))

    def test_no_log_file_path_is_provided(self):
        with self.assertRaises(SystemExit) as e:
            main(self.database_path)

    def test_receive_log_file_path_as_sys_argv(self):
        with mock.patch('sys.argv',
                        ['mail_log_parser',
                         self.short_log['path']]
                        ):
            self.assertEqual(receive_log_file_path(), self.short_log['path'])

    def test_receive_wrong_log_file_path(self):
        with self.assertRaises(SystemExit) as e:
            with mock.patch('sys.argv',
                            ['mail_log_parser',
                             'wrong_filepath_test_mail_log_parser']
                            ):
                receive_log_file_path()


if __name__ == '__main__':
    unittest.main()
