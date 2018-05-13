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

from pprint import pprint

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

    if len(languages) == 0:
        languages = ["en", "fr"]

    for l in languages:
        post_data.setdefault(fieldname_with_language("university_name", l), "")
        post_data.setdefault(fieldname_with_language("university_intro", l), "")

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
                "university_latlong":"0.0,0.0",
                "university_web_address": "www.some_university.com",
                'languages': [aloe.world.language] 
            }
        )

@aloe.step(u'the user pends those courses to that university')
def the_user_pends_addition_of_courses_to_university(step):
    with app.app_context():
        university = University.get_single(university_id = aloe.world.university_ids[0])
        university_data = university.request_dict()
        university_data.setlist("courses[]", [str(c) for c in aloe.world.course_ids])

        pprint(university_data)
        with app.test_request_context():
            aloe.world.response = aloe.world.app.post(
                "/university/" + str(aloe.world.university_ids[0]) + "/edit", 
                data=university_data
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

@aloe.step(u'the following university details are correct in response')
def the_following_university_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))["data"]

    expected_json = University.json_skeleton()
    expected_json = json.loads(step.multiline)

    for k, v in expected_json.items():
        assert_equals(v, returned_json[k])

@aloe.step(u'the following data is pending for that university')
def the_following_university_details_are_pending(step):
    with app.app_context():
        if aloe.world.last_pending_university_id is None:
            aloe.world.last_pending_university_id = UniversityPending.get_single(
                university_id=aloe.world.university_ids[0]
            )
        
        actual_json = aloe.world.last_pending_university_id.json()

        expected_json = University.json_skeleton()
        expected_json = json.loads(step.multiline)

        for k, v in expected_json.items():
            assert_equals(v, actual_json[k])

@aloe.step(u'the university \"([\w\d ]*)\" should exist in \"([\w\d ]*)\"')
def the_university_should_exist(step, university_name, language):
    with app.app_context():
        university = University.get_by_name(university_name=university_name, language=language)
        assert_equals(university.translations[language].university_name, university_name)

@aloe.step(u"the university \"([\w\d ]*)\" exists")
def the_university_exists(step, university_name):
    with app.app_context():
        try:
            uni = University.create({aloe.world.language: {"university_name": university_name}})
            aloe.world.university_ids.append(uni.university_id)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the university \"([\w\d ]*)\" is pending for addition")
def the_university_is_pending_for_addition(step, university_name):
    with app.app_context():
        try:
            aloe.world.last_pending_university_id = UniversityPending.addition(
                {aloe.world.language: {"university_name": university_name}},
                "0.0,0.0",
                "www.some_university.com"
            )
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the university \"([\w\d ]*)\" is pending for edit")
def the_university_is_pending_for_edit(step, university_name):
    with app.app_context():
        try:
            university = University.get_single(university_name=university_name, language=aloe.world.language)
            aloe.world.last_pending_university_id = UniversityPending.edit(university)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u"the translation \"([\w\d ]*)\" in \"([\w\d ]*)\" of university \"([\w\d ]*)\" is pending")
def the_translation_of_university_is_pending(step, translation, language, university_name):
    with app.app_context():
        try:
            university = University.get_single(university_name=university_name, language=aloe.world.language)
            aloe.world.last_pending_university_id = UniversityPending.edit(university)
            aloe.world.last_pending_university_id.set_translations(
                {language: {"university_name": translation}}
            )
            aloe.world.last_pending_university_id.save()

        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # University already in the system

@aloe.step(u'the university \"([\w\d ]*)\" should have the following data')
def the_university_has_data(step, university_name):
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language="en")
        expected_data = json.loads(step.multiline)
        assert_equals(university.json(), expected_data)

@aloe.step(u'the user pends the following data to it')
def the_user_pends_university_data_for_edit(step):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            "/university/" + str(aloe.world.university_ids[0]) + "/edit", 
            data=university_step_data_to_post_data(step.hashes)
        )

@aloe.step(u'those courses should be pending for addition')
def courses_should_be_pending_for_addition(step):
    with app.app_context():
        university = UniversityPending.get_single(university_id = aloe.world.university_ids[0])
        for course_id in aloe.world.course_ids:
            assert(university.has_course(course_id))
