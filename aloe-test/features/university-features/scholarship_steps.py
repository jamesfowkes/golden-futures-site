import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import University, UniversityPending
from app.models.scholarship import ScholarshipPending

@aloe.step(u'the user pends creation of scholarship \"([\w\d ]*)\" for university \"([\w\d ]*)\"')
def the_user_pends_creation_of_scholarship(step, scholarship, university_name):
    with app.test_request_context():
        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/scholarship/create'.format(university_id), 
            data={
                'university_id':university_id,
                'scholarship': scholarship,
                'language': aloe.world.language
            }
        )

@aloe.step(u'And the scholarship \"([\w\d ]*)\" should be pending for creation at \"([\w\d ]*)\"')
def the_scholarship_should_be_pending_for_creation(step, scholarship, university_name):
    with app.app_context():
        university = UniversityPending.get_single(university_name=university_name)
        pending_scholarships = ScholarshipPending.get(university=university).all()
        scholarship_strings = [scholarship.translations[aloe.world.language].scholarship_string for scholarship in pending_scholarships]
        assert(scholarship in scholarship_strings)

@aloe.step(u'And the scholarship \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_scholarship_should_exist(step, scholarship, university_name, language):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)
        scholarships = [f.scholarship_string for f in university.scholarships]
        assert(scholarship in scholarships)
