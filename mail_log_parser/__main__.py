import os

from .app import main


LOG_FILE = os.path.join(os.getcwd(), 'maillog')
main(LOG_FILE)