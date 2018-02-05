import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import University, UniversityPending
from app.models.contact_detail import ContactDetailPending

@aloe.step(u'the user pends creation of contact details \"([\w\d ]*)\" for university \"([\w\d ]*)\"')
def the_user_pends_creation_of_contact_detail(step, contact_detail, university_name):
    with app.test_request_context():
        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

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

@aloe.step(u'And the contact detail \"([\w\d ]*)\" should be pending for creation at \"([\w\d ]*)\"')
def the_contact_detail_should_be_pending_for_creation(step, contact_detail, university_name):
    with app.app_context():
        university = UniversityPending.get_single(university_name=university_name)
        pending_contact_details = ContactDetailPending.get(university=university).all()
        contact_detail_strings = [contact_detail.translations[aloe.world.language].contact_detail_string for contact_detail in pending_contact_details]
        assert(contact_detail in contact_detail_strings)

@aloe.step(u'And the contact detail \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_contact_detail_should_exist(step, contact_detail, university_name, language):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)
        contact_details = [f.contact_detail_string for f in university.contact_details]
        assert(contact_detail in contact_details)