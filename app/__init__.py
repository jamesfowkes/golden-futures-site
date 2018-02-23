import os
import logging
import logging.handlers

from flask import Flask

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

# Initialise blueprints after the views have been imported to correctly register endpoints
from app.blueprints import common
from app.blueprints import website
from app.blueprints import website_dashboard

website.init_app(app)
website_dashboard.init_app(app)
