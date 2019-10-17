from collections import defaultdict
import unittest

from .context import app
from app.data_manager import ManageData


def get_fields(ID='D69F5DF04F4',
               client_email='krasteplokomplekt@yandex.ru',
               receiver='arsenal-krsk@mail.ru',):
    pass # TODO


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
            self.ID: {'client_email': self.CLIENT_EMAIL ,
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
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 0})

    def test_manage_email_tracker_new_email_one_sent(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_SUCCESS)
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 1})
    
    def test_manage_email_tracker_old_email_one_more_sent(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_SUCCESS)
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)

        self.manager.manage_queue_tracker(self.FIELDS_BACKUP_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_BACKUP_SEND_ATTEMPT_SUCCESS)
        self.manager.manage_queue_tracker(self.FIELDS_BACKUP_CLOSE_QUEUE)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 2})
    
    def test_manage_email_tracker_two_receivers_two_sent_two_attempts(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_FAIL)
        for receiver in [self.RECEIVER, self.BACKUP_RECEIVER]:
            self.manager.manage_queue_tracker([
                ('ID', self.ID),
                ('receivers', receiver),
                ('status', 'sent')
            ])
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)
        self.assertEqual(self.MOCK_EMAIL_TRACKER, {self.CLIENT_EMAIL: 2})


class TestManageDeliveryTracker(TestManageQueueTracker, unittest.TestCase):
    def test_manage_delivery_tracker(self):
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_FAIL)
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_OPEN_QUEUE)
        self.manager.manage_queue_tracker(self.FIELDS_SEND_ATTEMPT_SUCCESS)
        self.manager.manage_queue_tracker(self.FIELDS_CLOSE_QUEUE)
        self.assertEqual(self.MOCK_DELIVERY_TRACKER,
                        {'undelivered': 1, 'delivered': 1})


if __name__ == '__main__':
    unittest.main()
