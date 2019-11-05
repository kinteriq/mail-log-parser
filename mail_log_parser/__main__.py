import os

from .app import main


main(os.path.join(os.getcwd(), 'results.db'))