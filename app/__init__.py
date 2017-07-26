import os

from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ["GF_CONFIG_CLASS"])

from app import encrypt
encrypt.init_app(app)

from app import database 
database.init_app(app)

from app.models import user
user.init_app(app)

from app.views import user
from app.views import dashboard
from app.views import index
