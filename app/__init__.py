import os
import logging
import logging.handlers

from pathlib import Path

from flask import Flask

THIS_PATH = Path(__file__).parent

static_file_list = []
for directory, subdirectories, files in os.walk(str(Path(THIS_PATH, "static"))):
    for file in files:
        static_file_list.append(Path(directory, file))

def static_url_exists(url):
    local_path = THIS_PATH / url
    return local_path in static_file_list

app = Flask(__name__)

app.config.from_object(os.environ["GF_CONFIG_CLASS"])

log_level = app.config["DEBUG"]
logfile = app.config["LOGFILE"]

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
handler.setLevel(log_level)
root_logger = logging.getLogger()
root_logger.addHandler(handler)

from app import encrypt
encrypt.init_app(app)

from app import locale
locale.init_app(app)

from app import database 
database.init_app(app)

from app import session
session.init_app(app)

from app.models import user
user.init_app(app)

from app.views import user
from app.views import category
from app.views import university
from app.views import course
from app.views import facility
from app.views import contact_detail
from app.views import admission
from app.views import tuition_fee
from app.views import scholarship
from app.views import quote

# Initialise blueprints after the views have been imported to correctly register endpoints
from app.blueprints import common
from app.blueprints import website
from app.blueprints import dashboard
from app.blueprints import categories_dashboard
from app.blueprints import courses_dashboard
from app.blueprints import universities_dashboard

website.init_app(app)
dashboard.init_app(app)
