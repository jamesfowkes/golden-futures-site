import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.university import University

@aloe.step(u'the user adds the scholarship \"([\w\d>% ]*)\" to university \"([\w\d ]*)\"')
def the_user_creates_the_scholarship(step, scholarship, university_name):

    with app.test_request_context():

        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/scholarship/create'.format(university_id), 
            data={'university_id':university_id, 'scholarship': scholarship},
            headers=[("Accept-Language", aloe.world.language)]
        )

@aloe.step(u'the following scholarships are returned:')
def the_following_scholarship_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("scholarship_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'And the scholarship \"([\w\d>% ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_scholarship_should_exist(step, scholarship, university_name, language):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)

        exists = any([f.scholarship_string == scholarship for f in university.scholarships])
        assert exists