import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app.application import app
from app.database import db

from app.models.user import User
from app.models.course import Course
from app.models.category import Category

@aloe.step(u"the user adds the course \"([\w\d ]*)\" to category \"([\w\d ]*)\"")
def add_course(step, course_name, category_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            '/course/create', 
            data={'course_name':course_name, "category_name": category_name}
        )

@aloe.step(u'the following course details are returned:')
def and_the_following_course_details(step):
    assert_equals(step.hashes[0], json.loads(aloe.world.response.data.decode("utf-8")))

@aloe.step(u"the course \"([\w\d ]*)\" exists in category \"([\w\d ]*)\"")
def create_course(step, course, category_name):
    try:
        Course.create(course_name=course, category_name=category_name)
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback() # Category already in the system

@aloe.step(u'the course \"([\w\d ]*)\" should exist')
def and_the_following_course_details(step, course_name):
    course = Course.get_single(course_name=course_name)
    assert_equals(course.course_name, course_name)
