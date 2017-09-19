""" runner.py 

Usage:
    runner.py --debug
"""

import docopt
import logging

from flask import url_for

from app import app

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    debug = args.get("--debug", None) is not None

    app.run(debug=debug)
    