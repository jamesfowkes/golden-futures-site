import os
import json

os.environ["GF_CONFIG_CLASS"] = "config.AloeConfig"

import aloe 
from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.encrypt import bcrypt
from app.database import db

from app.models.user import User

@aloe.before.all
def before_all():
    db.create_all()
    aloe.world.app = app.test_client()

@aloe.step(u"the admin user is in the system")
def create_admin_user(step):
    try:
        User.create('admin', 'Admin Smith', bcrypt.generate_password_hash('admin'), True)
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback() # User already in the system

@aloe.step(u"the admin user is logged in")
def login_admin_user(step):
    aloe.world.app.post(
        '/user/login', 
        data={'username': 'admin', 'password': 'admin'},
        follow_redirects=True
    )

@aloe.step(u"when the admin user creates standard user")
def create_standard_user(step):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/user/create',
            data={
                'username': step.hashes[0]["username"],
                'given_name': step.hashes[0]["given_name"],
                'password': step.hashes[0]["password"]
            }
        )

@aloe.step(u'Then I should get a \'(.*)\' response')
def then_i_should_get_response(step, expected_status_code):
    assert_equals(aloe.world.response.status_code, int(expected_status_code))

@aloe.step(u'And the following user details are returned:')
def and_the_following_user_details(step):
    assert_equals(step.hashes[0], json.loads(aloe.world.response.data.decode("utf-8")))
    
@aloe.after.all
def after_all():
    os.remove(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""))