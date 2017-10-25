import logging
import json

import flask_login

from app.database import db
from app.encrypt import bcrypt

from app.models.base_model import BaseModel, DeclarativeBase

logger = logging.getLogger(__name__)

login_manager = flask_login.LoginManager()

def init_app(app):
    login_manager.init_app(app)
    
@login_manager.user_loader
def load_user(user_id):
    return User.get_single(username=user_id)


class User(BaseModel, DeclarativeBase, flask_login.UserMixin):
    
    __tablename__ = "User"

    username = db.Column(db.String(80), primary_key=True)
    given_name = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String)
    admin_flag = db.Column(db.Boolean)

    def __init__(self, username, given_name, password, is_admin):
        self.username = username
        self.given_name = given_name
        self.password = password
        self.admin_flag = is_admin

    ### Flask-Login required functions
    def get_id(self):
        return self.username
    
    def is_active(self):
        return True

    ### END Flask-Login required functions

    def is_admin(self):
        return self.admin_flag 

    def login(self):
        flask_login.login_user(self)

    def logout(self):
        flask_login.logout_user()

    def match_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User %r, Name '%s', Admin: %s>" % (self.username, self.given_name, "yes" if self.is_admin() else "no")

    def json(self):
        return {
            "username": self.username,
            "given_name": self.given_name
        }

    @classmethod
    def create(cls, username, given_name, password, is_admin):
        password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = cls(username, given_name, password, is_admin)
        db.session.add(user)
        db.session.commit()
        return user
