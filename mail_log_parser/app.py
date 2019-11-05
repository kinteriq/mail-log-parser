import os
import sys

from .data import QUEUE_TRACKER, EMAIL_TRACKER, DELIVERY_TRACKER
from .parser import ParseLogLine
from .data_manager import ManageData


DATA = {
    'queue_tracker_db': QUEUE_TRACKER,
    'email_tracker_db': EMAIL_TRACKER,
    'delivery_tracker_db': DELIVERY_TRACKER,
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


def receive_log_file_path():
    log_filepath = os.path.join(os.getcwd(), 'maillog')
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            log_filepath = sys.argv[1]
        else:
            raise SystemExit(f'No such file: {sys.argv[1]}')
    return log_filepath
