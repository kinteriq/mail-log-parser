import os
import sys

from .data import QUEUE_TRACKER, EMAIL_TRACKER, DELIVERY_TRACKER
from .parser import ParseLogLine
from .data_manager import ManageData


DATA = {
    'queue_tracker_db': QUEUE_TRACKER,
    'email_tracker_db': EMAIL_TRACKER,
    'delivery_tracker': DELIVERY_TRACKER,
}


def main():
    filepath = receive_log_file_path()
    db_manager = ManageData(**DATA)
    with open(filepath, 'r') as log:
        line = log.readline()
        while line:
            parse_log_line = ParseLogLine(line)
            parsed = parse_log_line.parser()
            if parsed:
                db_manager.manage_queue_tracker(parsed)
            line = log.readline()
    print_email_tracker_results(db_manager)
    print_delivery_tracker_results(db_manager)


def receive_log_file_path():
    log_filepath = os.path.join(os.getcwd(), 'maillog')
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            log_filepath = sys.argv[1]
        else:
            raise SystemExit(f'No such file: {sys.argv[1]}')
    return log_filepath


def print_email_tracker_results(data):
    print('\nEmail tracker results:\n')
    for client_email, num_of_letters_sent in data.email_tracker_db.items():
        if not client_email:
            client_email = 'SERVER'
        print(f'\t<{client_email}> sent {num_of_letters_sent} letter(s).')


def print_delivery_tracker_results(data):
    delivered = data.delivery_tracker_db['delivered']
    undelivered = data.delivery_tracker_db['undelivered']
    print('\nDelivery tracker results:\n')
    print(f'\tDelivered: {delivered} letter(s).')
    print(f'\tUndelivered: {undelivered} letter(s).')