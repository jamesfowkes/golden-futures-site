import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.user import User

@aloe.step(u"when the user creates (admin|standard) user:")
def create_a_user(step, user_type):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/user/create',
            data={
                'username': step.hashes[0]["username"],
                'given_name': step.hashes[0]["given_name"],
                'password': step.hashes[0]["password"],
                'is_admin' : user_type == "admin",
                'language': aloe.world.language
            }
        )

@aloe.step(u"the (admin|standard|french) user is ((?:not )?logged) in")
def login_user(step, user_type, login_or_out):

    with app.test_request_context():
        if user_type == "standard":
            data={'username': 'standard', 'password': 'standard'}
        elif user_type == "admin":
            data={'username': 'admin', 'password': 'admin'}
        elif user_type == "french":
            data={'username': 'ordinaire', 'password': 'standard'}

        if login_or_out == "logged":
            aloe.world.app.post(
                '/user/login', 
                data=data,
                follow_redirects=False
            )
        elif login_or_out == "not logged":
            aloe.world.app.get(
                '/user/logout', 
                follow_redirects=False
            )

@aloe.step(u'And the following user details are returned:')
def and_the_following_user_details(step):
    assert_equals(step.hashes[0], json.loads(aloe.world.response.data.decode("utf-8")))
    
@aloe.step(u'a login attempt is made with credentials:')
def try_login_with_credentials(step):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
                '/user/login', 
                data=step.hashes[0],
                follow_redirects=False
        )

@aloe.step(u"the user deletes the (admin|standard) user")
def delete_a_user(step, user_type):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/user/delete',
            data={
                'username': user_type
            }
        )
