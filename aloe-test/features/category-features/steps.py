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

def split_course_list(courses):
    if len(courses) == 0:
        return []

    return [c.strip() for c in courses.split(",")]

@aloe.step(u"the user creates the category \"([\w\d ]*)\"")
def the_user_creates_the_category(step, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/category/create', 
            data={'category_name':category_name}
        )

@aloe.step(u"the user deletes the category \"([\w\d ]*)\"")
def the_user_deletes_the_category(step, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/category/delete', 
            data={'category_name':category_name}
        )

@aloe.step(u"the category \"([\w\d ]*)\" exists")
def the_category_exists(step, category):
    with app.app_context():
        try:
            Category.create(category_name=category)
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # Category already in the system

@aloe.step(u'the following category details are returned:')
def and_the_following_user_details_are_returned(step):
    expected = [{
        "category_name" : c["category_name"],
        "courses": split_course_list(c["courses"])
    } for c in step.hashes]
    assert_equals(expected, [json.loads(aloe.world.response.data.decode("utf-8"))])

@aloe.step(u'the category \"([\w\d ]*)\" should exist')
def the_category_should_exist(step, category_name):
    category = Category.get_single(category_name=category_name)
    assert_equals(category.category_name, category_name)

@aloe.step(u'the category \"([\w\d ]*)\" should not exist')
def the_category_should_exist(step, category_name):
    with app.app_context():
        category = Category.get_single(category_name=category_name)
        assert_equals(None, category)

@aloe.step(u'the category \"([\w\d ]*)\" should have the courses:')
def the_category_should_have_the_courses(step, category_name):
    with app.app_context():
        category = Category.get_single(category_name=category_name)
        expected_courses = [course["course_name"] for course in step.hashes]
        actual_courses = category.json(aloe.world.language)["courses"]
        assert_equals(expected_courses, actual_courses)
