from collections import defaultdict
import os
import sqlite3
import unittest

from .context import mail_log_parser
from mail_log_parser.data_manager import ManageData, ManageDatabase


class TestManageQueueTracker(unittest.TestCase):
    def setUp(self):
        self.MOCK_QUEUE_TRACKER = defaultdict(lambda:
            {'client_email': '', 'receivers': {}})
        self.MOCK_EMAIL_TRACKER = {}
        self.MOCK_DELIVERY_TRACKER = {'delivered': 0,
                                      'undelivered': 0}
        self.manager = ManageData(self.MOCK_QUEUE_TRACKER,
                                  self.MOCK_EMAIL_TRACKER,
                                  self.MOCK_DELIVERY_TRACKER)
        self.ID = 'D69F5DF04F4'
        self.BACKUP_ID = 'OPQF5DF04F4'
        self.CLIENT_EMAIL = 'krasteplokomplekt@yandex.ru'
        self.BACKUP_CLIENT_EMAIL = 'oksana_b@kubometr-samara.ru'
        self.RECEIVER = 'arsenal-krsk@mail.ru'
        self.BACKUP_RECEIVER = 'oksana_b@kubometr-samara.ru'
        self.FIELDS_OPEN_QUEUE = [
            ('ID', self.ID),
            ('client_email', self.CLIENT_EMAIL)
        ]
        self.FIELDS_BACKUP_OPEN_QUEUE = [
            ('ID', self.BACKUP_ID),
            ('client_email', self.CLIENT_EMAIL)
        ]
        self.FIELDS_SERVER_OPEN_QUEUE = [
            ('ID', self.ID),
            ('client_email', '')
        ]
        self.FIELDS_SEND_ATTEMPT_SUCCESS = [
            ('ID', self.ID),
            ('receivers', self.RECEIVER),
            ('status', 'sent')
        ]
        self.FIELDS_BACKUP_SEND_ATTEMPT_SUCCESS = [
            ('ID', self.BACKUP_ID),
            ('receivers', self.RECEIVER),
            ('status', 'sent')
        ]
        self.FIELDS_SEND_ATTEMPT_FAIL = [
            ('ID', self.ID),
            ('receivers', self.RECEIVER),
            ('status', 'bounced')
        ]
        self.FIELDS_CLOSE_QUEUE = [('ID', self.ID)]
        self.FIELDS_BACKUP_CLOSE_QUEUE = [('ID', self.BACKUP_ID)]

    def test_manage_queue_tracker_with_open_queue_group(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.assertEqual(self.MOCK_QUEUE_TRACKER, {
            self.ID: {'client_email': self.CLIENT_EMAIL,
                      'receivers': {}}
        })

    def test_manage_queue_tracker_with_server_queue_group(self):
        self.manager.manage_queue_tracker(self.FIELDS_SERVER_OPEN_QUEUE)
        self.assertEqual(self.MOCK_QUEUE_TRACKER, {
            self.ID: {'client_email': '', 'receivers': {}}
        })
    
    def test_manage_queue_tracker_with_send_attempt_success_group(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_SUCCESS)
        self.assertEqual(self.MOCK_QUEUE_TRACKER, {
            self.ID: {
                'client_email': self.CLIENT_EMAIL,
                'receivers': {self.RECEIVER: 1}}
        })

    def test_manage_queue_tracker_with_send_attempt_fail_group(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_FAIL)
        self.assertEqual(self.MOCK_QUEUE_TRACKER, {
            self.ID: {
                'client_email': self.CLIENT_EMAIL,
                'receivers': {self.RECEIVER: 0}}
        })
    
    def test_manage_queue_tracker_with_failed_and_successful_send_attempts_groups(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_FAIL)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_SUCCESS)
        self.assertEqual(self.MOCK_QUEUE_TRACKER, {
            self.ID: {
                'client_email': self.CLIENT_EMAIL,
                'receivers': {self.RECEIVER: 1}}
        })
    
    def test_manage_queue_tracker_with_close_queue_group(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_SUCCESS)
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)
        self.assertNotIn(self.ID, self.MOCK_QUEUE_TRACKER)


class TestManageEmailTracker(TestManageQueueTracker, unittest.TestCase):
    def test_manage_email_tracker_new_email_nothing_sent(self):
        self.manager.queue_tracker_db = {
            1: {'client_email': self.CLIENT_EMAIL, 'receivers': {} }
        }
        self.manager.manage_email_tracker(1)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 0})

    def test_manage_email_tracker_new_email_one_sent(self):
        self.manager.queue_tracker_db = {
            1: {'client_email': self.CLIENT_EMAIL,
                'receivers': {'receiver': 1}
        }}
        self.manager.manage_email_tracker(1)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 1})
    
    def test_manage_email_tracker_old_email_one_more_sent(self):
        self.manager.queue_tracker_db = {
            1: {'client_email': self.CLIENT_EMAIL,
                'receivers': {'receiver': 1}
        }}
        self.manager.manage_email_tracker(1)

        self.manager.queue_tracker_db = {
            2: {'client_email': self.CLIENT_EMAIL,
                'receivers': {'receiver': 1}
        }}
        self.manager.manage_email_tracker(2)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 2})
    
    def test_manage_email_tracker_two_receivers_two_sent_two_attempts(self):
        self.manager.queue_tracker_db = {
            1: {'client_email': self.CLIENT_EMAIL,
                'receivers': {'receiver_1': 0}
        }}
        self.manager.manage_email_tracker(1)

        self.manager.queue_tracker_db = {
            2: {'client_email': self.CLIENT_EMAIL,
                'receivers': {'receiver_2': 1}
        }}
        self.manager.manage_email_tracker(2)

        self.manager.queue_tracker_db = {
            3: {'client_email': self.CLIENT_EMAIL,
                'receivers': {'receiver_1': 1}
        }}
        self.manager.manage_email_tracker(3)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 2})


class TestManageDeliveryTracker(TestManageQueueTracker, unittest.TestCase):
    def test_manage_delivery_tracker(self):
        self.manager.queue_tracker_db= {
            1: {'client_email': '', 'receivers': {'receiver_email_1': 1,
                                                  'receiver_email_2': 0,} }
        }
        self.manager.manage_delivery_tracker(1)
        self.assertEqual(self.MOCK_DELIVERY_TRACKER,
                        {'undelivered': 1, 'delivered': 1})


class TestManageDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database_path = os.path.join(os.getcwd(), 'test_manage_database.db')
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.database_path):
            os.remove(cls.database_path)

    def _execute_command(self, *command):
        con = sqlite3.connect(self.database_path)
        cursor = con.cursor()
        result = cursor.execute(*command)
        if result:
            result = result.fetchall()
        con.commit()
        con.close()
        return result

    def test_email_tracker_transfer_data_ok(self):
        self._execute_command('''CREATE TABLE IF NOT EXISTS email_tracker
            (client_email TEXT PRIMARY KEY, num_of_letters_sent INTEGER)''')
        db_manager = ManageDatabase(
            path=self.database_path,
            queue_tracker_db=None,
            email_tracker_db={'test@test.com': 12},
            delivery_tracker_db=None
        )
        db_manager.transfer_data()
        
        self.assertEqual(
            self._execute_command('SELECT * FROM email_tracker'),
            [('test@test.com', 12)]
        )


if __name__ == '__main__':
    unittest.main()
