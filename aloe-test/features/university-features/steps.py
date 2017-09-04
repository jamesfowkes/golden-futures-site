import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.university import University

@aloe.step(u'the user adds the university \"([\w\d ]*)\"')
def the_user_creates_the_university(step, university_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            "/" + aloe.world.language + '/university/create', 
            data={'university_name':university_name}
        )

@aloe.step(u'the following university details are returned:')
def the_following_university_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("university_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'the university \"([\w\d ]*)\" should exist')
def the_university_should_exist(step, university_name):
    with app.app_context():
        universities = University.get_by_name(university_name=university_name)
        assert_equals(len(universities), 1)
        assert_equals(universities[0].university_name, university_name)