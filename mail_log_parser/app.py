import os
import sys

from .data import QUEUE_TRACKER, EMAIL_TRACKER, DELIVERY_TRACKER
from .parser import ParseLogLine
from .data_manager import ManageData, ManageDatabase


_DATA = {
    'queue_tracker_db': QUEUE_TRACKER,
    'email_tracker_db': EMAIL_TRACKER,
    'delivery_tracker_db': DELIVERY_TRACKER,
}


def main(database_path):
    filepath = receive_log_file_path()
    db_manager = ManageDatabase(path=database_path, **_DATA)
    with open(filepath, 'r') as log:
        line = log.readline()
        while line:
            parse_log_line = ParseLogLine(line)
            parsed = parse_log_line.parser()
            if parsed:
                db_manager.manage_queue_tracker(parsed)
            line = log.readline()
    db_manager.create_db()
    db_manager.transfer_data()
    print(f'Results are saved in "{database_path}"')


def receive_log_file_path():
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            log_filepath = sys.argv[1]
        else:
            raise SystemExit(f'No such file: {sys.argv[1]}')
    else:
        raise SystemExit('Path to log file is not provided')
    return log_filepath
