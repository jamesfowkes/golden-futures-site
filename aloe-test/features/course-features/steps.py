import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.user import User
from app.models.course import Course, CoursePending
from app.models.category import Category, CategoryPending

@aloe.step(u"the user adds the course \"([\w\d ]*)\" to category \"([\w\d ]*)\"")
def the_user_adds_the_course(step, course_name, category_name):
    with app.test_request_context():
        category_id = CategoryPending.get_single(category_name=category_name).category_id
        aloe.world.response = aloe.world.app.post(
            '/course/create', 
            data={
                'course_name':course_name,
                "category_id": str(category_id),
                "language": aloe.world.language
            }
        )

@aloe.step(u'the following course details are returned:')
def the_following_course_details_are_returned(step):
    assert_equals(step.hashes[0], json.loads(aloe.world.response.data.decode("utf-8")))

@aloe.step(u"the course \"([\w\d ]*)\" exists in category \"([\w\d ]*)\"")
def the_course_exists_in_category(step, course, category_name):
    with app.app_context():
        category = Category.get_single(category_name=category_name)
        course = Course.get_single(course_name=course, language=aloe.world.language)
        if course is None:
            course = Course.create(course_name=course, language=aloe.world.language)
        
        #except sqlalchemy.exc.IntegrityError:
        #    db.session.rollback() # Course already in the system
        
        category.add_course(course)       

@aloe.step(u'the course \"([\w\d ]*)\" should exist')
def the_course_should_exist(step, course_name):
    with app.app_context():
        course = CoursePending.get_single(course_name=course_name, language=aloe.world.language)
        assert_equals(course.translations[aloe.world.language].course_name, course_name)

@aloe.step(u'the course \"([\w\d ]*)\" should have the translations')
def the_course_should_have_the_translations(step, course_name):
    with app.app_context():
        courses = CoursePending.get_translations(course_name=course_name, language=aloe.world.language)
        assert_equals(course.all_translations(), step.hashes[0])