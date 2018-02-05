import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import University, UniversityPending
from app.models.admission import AdmissionPending
        
@aloe.step(u'the user pends creation of admission \"([\w\d ]*)\" for university \"([\w\d ]*)\"')
def the_user_pends_creation_of_admission(step, admission, university_name):
    with app.test_request_context():
        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/admission/create'.format(university_id), 
            data={
                'university_id':university_id,
                'admission': admission,
                'language': aloe.world.language
            }
        )

@aloe.step(u'the following admissions are returned:')
def the_following_admission_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("admission_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'And the admission \"([\w\d ]*)\" should be pending for creation at \"([\w\d ]*)\"')
def the_admission_should_be_pending_for_creation(step, admission, university_name):
    with app.app_context():
        university = UniversityPending.get_single(university_name=university_name)
        pending_admissions = AdmissionPending.get(university=university).all()
        admission_strings = [admission.translations[aloe.world.language].admission_string for admission in pending_admissions]
        print(pending_admissions[0].admission_string)
        print(admission_strings)
        assert(admission in admission_strings)

@aloe.step(u'And the admission \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_admission_should_exist(step, admission, university_name, language):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=university_name, language=aloe.world.language)

        exists = any([f.admission_string == admission for f in university.admissions])
        assert exists