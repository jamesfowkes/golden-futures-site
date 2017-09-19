import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.university import University
from app.models.admission import Admission

@aloe.step(u'the user adds the admission \"([\w\d ]*)\" to university \"([\w\d ]*)\"')
def the_user_creates_the_admission(step, admission, university_name):

    with app.test_request_context():

        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/admission/create'.format(university_id), 
            data={'university_id':university_id, 'admission': admission},
            headers=[("Accept-Language", aloe.world.language)]
        )

@aloe.step(u'the following admissions are returned:')
def the_following_admission_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("admission_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'And the admission \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_admission_should_exist(step, admission, university_name, language):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)

        exists = any([f.admission_string == admission for f in university.admissions])
        assert exists