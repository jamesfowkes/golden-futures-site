import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.university import University
from app.models.facility import Facility

@aloe.step(u'the user adds the facility \"([\w\d ]*)\" to university \"([\w\d ]*)\"')
def the_user_creates_the_facility(step, facility, university_name):

    with app.test_request_context():

        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/facility/create'.format(university_id), 
            data={'university_id':university_id, 'facility': facility},
            headers=[("Accept-Language", aloe.world.language)]
        )

@aloe.step(u'the following facility details are returned:')
def the_following_facility_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("facility_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'And the facility \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_facility_should_exist(step, facility, university_name, language):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)
        exists = any([f.facility_string == facility for f in university.facilities])
        assert exists