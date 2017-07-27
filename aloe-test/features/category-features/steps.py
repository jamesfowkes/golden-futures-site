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

@aloe.step(u"the user adds the category \"([\w\d ]*)\"")
def add_category(step, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/category/create', 
            data={'category_name':category_name}
        )

@aloe.step(u"the category \"([\w\d ]*)\" exists")
def create_category(step, category):
    try:
        Category.create(category_name=category)
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback() # Category already in the system

@aloe.step(u'the following category details are returned:')
def and_the_following_user_details(step):
    expected = [{
        "category_name" : c["category_name"],
        "courses": split_course_list(c["courses"])
    } for c in step.hashes]
    assert_equals(expected, [json.loads(aloe.world.response.data.decode("utf-8"))])

@aloe.step(u'the category \"([\w\d ]*)\" should exist')
def and_the_following_user_details(step, category_name):
    category = Category.get_single(category_name=category_name)
    assert_equals(category.category_name, category_name)

@aloe.step(u'the category \"([\w\d ]*)\" should have the courses:')
def the_category_should_have_the_courses(step, category_name):
    category = Category.get_single(category_name=category_name)
    expected_courses = [course["course_name"] for course in step.hashes]
    actual_courses = category.json()["courses"]
    assert_equals(expected_courses, actual_courses)
