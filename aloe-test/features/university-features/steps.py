import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import UniversityPending

@aloe.step(u'the user adds the university \"([\w\d ]*)\"')
def the_user_creates_the_university(step, university_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/university/create', 
            data={
                'university_name':university_name,
                'language': aloe.world.language
            }
        )

@aloe.step(u'the following university details are returned:')
def the_following_university_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("university_id")
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'the university \"([\w\d ]*)\" should exist in \"([\w\d ]*)\"')
def the_university_should_exist(step, university_name, language):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=university_name, language=language)
        assert_equals(university.translations[language].university_name, university_name)

@aloe.step(u"the university \"([\w\d ]*)\" exists in \"([\w\d ]*)\"")
def the_university_exists(step, university_name, language):
    with app.app_context():
        try:
            UniversityPending.create(university_name=university_name, language=language)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the user adds the translation \"([\w\d ]*)\" to university \"([\w\d ]*)\"")
def the_user_adds_the_university_translation(step, translation, university_name):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=university_name, language="en")
        aloe.world.response = aloe.world.app.post(
            "/university/" + str(university.university_id) + "/translate", 
            data={
                'university_name':translation,
                'language':aloe.world.language
            }
        )

@aloe.step(u'the university \"([\w\d ]*)\" should have \"([\w\d ]*)\" translation \"([\w\d ]*)\"')
def the_universities_should_have_the_same_id(step, english_name, language, translated_name):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=english_name, language="en")
        assert_equals(university.translations[language].university_name, translated_name)
