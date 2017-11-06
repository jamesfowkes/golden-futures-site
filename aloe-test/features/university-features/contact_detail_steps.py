import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import UniversityPending
from app.models.contact_detail import ContactDetail

@aloe.step(u'the user adds the contact detail \"([\w\d @.]*)\" to university \"([\w\d ]*)\"')
def the_user_creates_the_contact_detail(step, contact_detail, university_name):

    with app.test_request_context():

        university_id = UniversityPending.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/contact_detail/create'.format(university_id), 
            data={
                'university_id':university_id,
                'contact_detail': contact_detail,
                'language': aloe.world.language
            }
        )

@aloe.step(u'the following contact details are returned:')
def the_following_contact_detail_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("contact_detail_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'And the contact detail \"([\w\d @.]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_contact_detail_should_exist(step, contact_detail, university_name, language):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=university_name, language=aloe.world.language)
        exists = any([f.contact_detail_string == contact_detail for f in university.contact_details])
        assert exists
