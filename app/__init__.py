import os

from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ["GF_CONFIG_CLASS"])

from app import encrypt
encrypt.init_app(app)

from app import locale
locale.init_app(app)

from app import database 
database.init_app(app)

from app.models import user
user.init_app(app)

from app.views import user
from app.views import dashboard
from app.views import index
from app.views import course
from app.views import category
from app.views import university
from app.views import facility
from app.views import contact_detail
from app.views import admission
from app.views import tuition_fee
from app.views import scholarship
