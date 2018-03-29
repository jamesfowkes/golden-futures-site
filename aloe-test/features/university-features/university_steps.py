import os

import json

import aloe

from werkzeug.datastructures import MultiDict

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import University, UniversityPending

from ..steps import fieldname_with_language

def university_step_data_to_post_data(step_data):

    post_data = MultiDict()
    languages = []
    for data_dict in step_data:
        language = data_dict.pop("language")
        languages.append(language)
        for k, v in data_dict.items():
            if University.is_translatable(k):
                k = k + "[" + language + "]"
            post_data.add(k, v)

    post_data.setdefault("university_latlong", "")
    post_data.setdefault("university_web_address", "")

    post_data["languages"] = ",".join(languages)

    return post_data

@aloe.step(u'the user pends addition of university \"([\w\d ]*)\"')
def the_user_pends_addition_of_university(step, university_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/university/create', 
            data={
                fieldname_with_language("university_name", aloe.world.language):university_name,
                fieldname_with_language("university_intro", aloe.world.language):"A new university",
                'languages': [aloe.world.language] 
            }
        )

@aloe.step(u'the user approves pending changes to university \"([\w\d ]*)\"')
def the_user_approves_pending_changes_to_university(step, university_name):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=university_name, language=aloe.world.language)
        aloe.world.response = aloe.world.app.post(
            '/university/pending/approve', 
            data={
                'data_id':university.pending_id
            }
        )

@aloe.step(u'the following university details are correct in response:')
def the_following_university_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))["data"]

    expected_json = University.json_skeleton()
    expected_json = json.loads(step.multiline)

    for k, v in expected_json.items():
        assert_equals(v, returned_json[k])

@aloe.step(u'the university \"([\w\d ]*)\" should exist in \"([\w\d ]*)\"')
def the_university_should_exist(step, university_name, language):
    with app.app_context():
        university = University.get_by_name(university_name=university_name, language=language)
        assert_equals(university.translations[language].university_name, university_name)

@aloe.step(u"the university \"([\w\d ]*)\" exists")
def the_university_exists(step, university_name):
    with app.app_context():
        try:
            University.create({aloe.world.language: {"university_name": university_name}})
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the university \"([\w\d ]*)\" is pending for addition")
def the_university_is_pending_for_addition(step, university_name):
    with app.app_context():
        try:
            UniversityPending.addition(
                {aloe.world.language: {"university_name": university_name}}
            )
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the university \"([\w\d ]*)\" is pending for edit")
def the_university_is_pending_for_edit(step, university_name):
    with app.app_context():
        try:
            university = University.get_single(university_name=university_name, language=aloe.world.language)
            UniversityPending.edit(university)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the translation \"([\w\d ]*)\" in \"([\w\d ]*)\" of university \"([\w\d ]*)\" is pending")
def the_translation_of_university_is_pending(step, translation, language, university_name):
    with app.app_context():
        try:
            university = University.get_single(university_name=university_name, language=aloe.world.language)
            pending = UniversityPending.edit(university)
            pending.set_translations(
                {language: {"university_name": translation}}
            )
            pending.save()

        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u'the university \"([\w\d ]*)\" should have the following data')
def the_university_has_data(step, university_name):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language="en")
        expected_data = json.loads(step.multiline)
        assert_equals(university.json(), expected_data)

@aloe.step(u'the user pends the following data to university \"([\w\d ]*)\"')
def the_user_pends_university_data_for_edit(step, university_name):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language="en")
        aloe.world.response = aloe.world.app.post(
            "/university/" + str(university.university_id) + "/edit", 
            data=university_step_data_to_post_data(step.hashes)
        )
