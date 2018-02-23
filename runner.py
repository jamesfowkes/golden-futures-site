""" runner.py 

Usage:
    runner.py --debug
"""

import docopt
import logging

from app import app

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    debug = args.get("--debug", None) is not None

    if debug:
        logging.basicConfig(level=logging.INFO)
    else:
    	logging.basicConfig(level=logging.WARNING)
    	
    app.run(debug=debug)
    