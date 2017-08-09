import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.user import User
from app.models.category import Category

@aloe.step(u"the user creates the category \"([\w\d ]*)\"")
def the_user_creates_the_category(step, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            "/" + aloe.world.language + '/category/create', 
            data={'category_name':category_name}
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
            db.session.rollback() # Category already in the system

@aloe.step(u'the following category details are returned:')
def and_the_following_user_details_are_returned(step):
    assert_equals(step.hashes, (json.loads(aloe.world.response.data.decode("utf-8")),))

@aloe.step(u'the category \"([\w\d ]*)\" should exist in language \"([\w\d ]*)\"')
def the_category_should_exist_in_language(step, category_name, language):
    with app.app_context():
        category = Category.get_single(category_name=category_name, language=language)
        assert_equals(category.category_name, category_name)
        assert_equals(category.language, language)
        
@aloe.step(u'the category \"([\w\d ]*)\" should not exist')
def the_category_should_not_exist(step, category_name):
    with app.app_context():
        category = Category.get_single(category_name=category_name)
        assert_equals(None, category)

@aloe.step(u'the category \"([\w\d ]*)\" should have the courses:')
def the_category_should_have_the_courses(step, category_name):
    with app.app_context():
        category = Category.get_single(category_name=category_name)
        
        expected_courses = [course["course_name"] for course in step.hashes]
        expected_languages = [course["language"] for course in step.hashes]

        actual_courses = [c.course_name for c in category.courses]
        actual_languages = [c.language for c in category.courses]

        assert_equals(expected_courses, actual_courses)
        assert_equals(expected_languages, actual_languages)
