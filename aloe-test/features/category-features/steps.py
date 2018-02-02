import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.user import User
from app.models.category import Category, CategoryPending

@aloe.step(u"the user sets the category \"([\w\d ]*)\" as pending for creation")
def the_user_creates_the_category(step, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            "/category/create",
            data={
                "category_name": category_name,
                "category_intro": "Aloe test category introduction",
                "category_careers":  "Behaviour Driven Development",
                "language": aloe.world.language
            }
        )

@aloe.step(u"the category \"([\w\d ]*)\" should be pending for creation(?: in language \"([\w\d ]*)\")?")
def the_category_should_be_pending_for_creation(step, category_name, language):
    language = language or "en"
    with app.app_context():
        category = CategoryPending.get_single(category_name=category_name)
        assert_equals(category_name, category.category_name)
        assert_equals("add_edit", category.pending_type)
        assert_equals(None, category.category_id)
        assert_equals(language, category.current_language())

@aloe.step(u"the category \"([\w\d ]*)\" is pending for creation")
def the_category_is_pending_for_creation(step, category):
    with app.app_context():
        try:
            CategoryPending.addition(category, aloe.world.language)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # Category already pending

@aloe.step(u"the user accepts the creation of category \"([\w\d ]*)\"")
def the_user_accepts_the_creation_of_category(step, category_name):
       with app.test_request_context():
        category = CategoryPending.get_single(category_name=category_name)
        aloe.world.response = aloe.world.app.post(
            "/category/pending/approve",
            data={
                "data_id": category.pending_id
            }
        )

@aloe.step(u"the user deletes the category \"([\w\d ]*)\"")
def the_user_deletes_the_category(step, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            "/" + aloe.world.language + '/category/delete', 
            data={'category_name':category_name}
        )

@aloe.step(u"the category \"([\w\d ]*)\" exists")
def the_category_exists(step, category):
    with app.app_context():
        try:
            Category.create(category_name=category, language=aloe.world.language)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # Category already pending

@aloe.step(u"the category \"([\w\d ]*)\" is pending for deletion")
def the_category_is_pending_for_deletion(step, category_name):
    with app.app_context():
        try:
            category = Category.get_single(category_name=category_name)
            CategoryPending.deletion(category)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # Category already pending

@aloe.step(u'the following category details are returned:')
def and_the_following_category_details_are_returned(step):
    response = json.loads(aloe.world.response.data.decode("utf-8"))
    details = {
        "category_name": response['data']['category_name'],
        "language": response['data']['language'],
    }

    assert_equals(step.hashes, (details,))

@aloe.step(u'the category \"([\w\d ]*)\" should exist in language \"([\w\d ]*)\"')
def the_category_should_exist_in_language(step, category_name, language):
    with app.app_context():
        category = Category.get_single(category_name=category_name, language=language)
        assert_equals(category.translations[language].category_name, category_name)
        
@aloe.step(u'the category \"([\w\d ]*)\" should not exist')
def the_category_should_not_exist(step, category_name):
    with app.app_context():
        category = CategoryPending.get_single(category_name=category_name)
        assert_equals(None, category)

@aloe.step(u'the category \"([\w\d ]*)\" should have the courses:')
def the_category_should_have_the_courses(step, category_name):
    with app.app_context():
        category = CategoryPending.get_single(category_name=category_name)
        
        expected_course_names = [course["course_name"] for course in step.hashes]
        expected_course_languages = [course["language"] for course in step.hashes]

        actual_courses = {c.course_name: c for c in category.courses}

        assert_equals(set(expected_course_names), set(actual_courses.keys()))
        
        for (expected_course_name, expected_language) in zip(expected_course_names, expected_course_languages):
            actual_course_name = actual_courses[expected_course_name].translations[expected_language].course_name
            assert_equals(expected_course_name, actual_course_name)
