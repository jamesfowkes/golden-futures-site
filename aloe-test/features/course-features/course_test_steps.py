import logging

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

logger = logging.getLogger(__name__)

@aloe.step(u"the course \"([\w\d ]*)\" should be pending for creation(?: in language \"([\w\d ]*)\")?")
def the_course_should_be_pending_for_creation(step, course_name, language):
    language = language or "en"
    with app.app_context():
        pending_course = CoursePending.get_single(course_name=course_name)
        assert_equals(course_name, pending_course.course_name)
        assert_equals("add_edit", pending_course.pending_type)
        assert_equals(None, pending_course.course_id)
        assert_equals(language, pending_course.current_language())

@aloe.step(u"the course \"([\w\d ]*)\" should be pending for edit as \"([\w\d ]*)\"(?: in language \"([\w\d ]*)\")?")
def the_course_should_be_pending_for_edit(step, existing_course_name, new_course_name, language):
    language = language or "en"
    with app.app_context():
        course = Course.get_single(course_name=existing_course_name)
        pending_course = CoursePending.get_single(course_name=new_course_name, language=language)
        assert_equals(new_course_name, pending_course.course_name)
        assert_equals("add_edit", pending_course.pending_type)
        assert_equals(course.course_id, pending_course.course_id)
        assert_equals(language, pending_course.current_language())

@aloe.step(u"the course \"([\w\d ]*)\" is pending for creation")
def the_course_is_pending_for_creation(step, course):
    with app.app_context():
        try:
            CoursePending.addition({aloe.world.language: {"course_name": course}})
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback() # Course already pending
            raise(e)

@aloe.step(u'the course \"([\w\d ]*)\" is pending to be added to category \"([\w\d ]*)\"')
def the_course_is_pending_to_be_added_to_category(step, course_name, category_name):
    with app.app_context():
        pending_category = CategoryPending.get_single(category_name=category_name, language=aloe.world.language)
        if pending_category is None:
            category = Category.get_single(category_name=category_name, language=aloe.world.language)
            pending_category = CategoryPending.edit(category)

        course = Course.get_single(course_name=course_name, language=aloe.world.language)
        pending_category.add_course(course)

@aloe.step(u'the course \"([\w\d ]*)\" should be pending to be added to category \"([\w\d ]*)\"')
def the_course_should_be_pending_to_be_added_to_category(step, course_name, category_name):
    with app.app_context():
        pending_category = CategoryPending.get_single(category_name=category_name, language=aloe.world.language)
        assert(course_name in pending_category.course_names())

@aloe.step(u'the following course details are returned:')
def the_following_course_details_are_returned(step):
    response = json.loads(aloe.world.response.data.decode("utf-8"))
    details = {
        "course_name": response['data']['course_name'],
        "category_names": ", ".join(response['data']['category_names']),
        "language": response['data']['language'],
    }

    assert_equals(step.hashes[0], details)

@aloe.step(u"the course \"([\w\d ]*)\" exists")
def the_course_exists(step, course_name):
    with app.app_context():
        try:
            course = Course.create({aloe.world.language: {"course_name": course_name}})
            aloe.world.course_ids.append(course.course_id)

        except sqlalchemy.exc.IntegrityError:
            db.session.rollback() # Course already pending

@aloe.step(u"the course \"([\w\d ]*)\" is in category \"([\w\d ]*)\"")
def the_course_exists_in_category(step, course_name, category_name):
    with app.app_context():
        category = Category.get_single(category_name=category_name)
        course = Course.get_single(course_name=course_name)
        category.add_course(course)
        
@aloe.step(u'the course \"([\w\d ]*)\" should exist')
def the_course_should_exist(step, course_name):
    with app.app_context():
        course = Course.get_single(course_name=course_name, language=aloe.world.language)
        assert_equals(course.translations[aloe.world.language].course_name, course_name)

@aloe.step(u'the course \"([\w\d ]*)\" should not exist')
def the_course_should_exist(step, course_name):
    with app.app_context():
        course = Course.get_single(course_name=course_name, language=aloe.world.language)
        assert_equals(None, course)

@aloe.step(u'the course \"([\w\d ]*)\" should have the \"([\w\d ]*)\" translations')
def the_course_should_have_the_translations(step, course_name, language):
    with app.app_context():
        course = Course.get_single(course_name=course_name, language=aloe.world.language)
        translations = course.all_translations()
        assert_equals(translations[language], step.hashes[0])
