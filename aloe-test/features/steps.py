import os
import json

os.environ["GF_CONFIG_CLASS"] = "config.AloeConfig"

import aloe 
from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.user import User

@aloe.before.each_feature
def before_each_feature(feature):
    db.create_all()
    aloe.world.app = app.test_client()

@aloe.step(u"the (admin|standard) user is in the system")
def create_admin_user(step, user_type):
    try:
        if user_type == "standard":
            User.create('standard', 'Standard Smith', 'standard', False)
        elif user_type == "admin":
            User.create('admin', 'Admin Smith', 'admin', True)
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback() # User already in the system

@aloe.step(u"the (admin|standard) user is ((?:not )?logged) in")
def login_admin_user(step, user_type, login_or_out):

    if user_type == "standard":
        data={'username': 'standard', 'password': 'standard'}
    elif user_type == "admin":
        data={'username': 'admin', 'password': 'admin'}

    if login_or_out == "logged":
        aloe.world.app.post(
            '/user/login', 
            data=data,
            follow_redirects=True
        )
    elif login_or_out == "not logged":
        aloe.world.app.get(
            '/user/logout', 
            follow_redirects=True
        )

@aloe.step(u"when the user creates (admin|standard) user:")
def create_a_user(step, user_type):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/user/create',
            data={
                'username': step.hashes[0]["username"],
                'given_name': step.hashes[0]["given_name"],
                'password': step.hashes[0]["password"],
                'is_admin' : user_type == "admin"
            }
        )


@aloe.step(u'Then I should get a \'(.*)\' response')
def then_i_should_get_response(step, expected_status_code):
    assert_equals(aloe.world.response.status_code, int(expected_status_code))

@aloe.step(u'And the following user details are returned:')
def and_the_following_user_details(step):
    assert_equals(step.hashes[0], json.loads(aloe.world.response.data.decode("utf-8")))
    
@aloe.step(u'a login attempt is made with credentials:')
def try_login_with_credentials(step):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
                '/user/login', 
                data=step.hashes[0],
                follow_redirects=True
        )

@aloe.after.each_feature
def after_each_feature(feature):
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")

    if os.path.isfile(db_path):
        os.remove(db_path)
