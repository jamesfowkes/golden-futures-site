import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import University, UniversityPending
from app.models.facility import FacilityPending

@aloe.step(u'the user pends creation of facility \"([\w\d ]*)\" for university \"([\w\d ]*)\"')
def the_user_pends_creation_of_facility(step, facility, university_name):
    with app.test_request_context():
        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/facility/create'.format(university_id), 
            data={
                'university_id':university_id,
                'facility': facility,
                'language': aloe.world.language
            }
        )

@aloe.step(u'And the facility \"([\w\d ]*)\" should be pending for creation at \"([\w\d ]*)\"')
def the_facility_should_be_pending_for_creation(step, facility, university_name):
    with app.app_context():
        university = UniversityPending.get_single(university_name=university_name)
        pending_facilities = FacilityPending.get(university=university).all()
        facility_strings = [facility.translations[aloe.world.language].facility_string for facility in pending_facilities]
        assert(facility in facility_strings)

@aloe.step(u'And the facility \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_facility_should_exist(step, facility, university_name, language):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)
        facilities = [f.facility_string for f in university.facilities]
        assert(facility in facilities)