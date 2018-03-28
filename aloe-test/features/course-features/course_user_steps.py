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

from ..steps import fieldname_with_language

logger = logging.getLogger(__name__)

@aloe.step(u"the user sets the course \"([\w\d ]*)\" as pending for creation")
def the_user_sets_the_course_as_pending_for_creation(step, course_name):
    with app.test_request_context():
        aloe.world.response = aloe.world.app.post(
            "/course/create",
            data={
                fieldname_with_language("course_name", aloe.world.language): course_name,
                "languages": [aloe.world.language]
            }
        )

@aloe.step(u"the user accepts pending changes to course \"([\w\d ]*)\"")
def the_user_accepts_pending_changes_to_course(step, course_name):
    with app.test_request_context():
        pending_course = CoursePending.get_single(course_name=course_name)
        aloe.world.response = aloe.world.app.post(
            "/course/pending/approve",
            data={
                "data_id": pending_course.pending_id
            }
        )

@aloe.step(u"the user accepts the creation of course \"([\w\d ]*)\"")
def the_user_accepts_the_creation_of_course(step, course_name):
    with app.test_request_context():
        pending_course = CoursePending.get_single(course_name=course_name)
        aloe.world.response = aloe.world.app.post(
            "/course/pending/approve",
            data={
                "data_id": pending_course.pending_id
            }
        )

@aloe.step(u"the user pends addition of course \"([\w\d ]*)\" to category \"([\w\d ]*)\"")
def the_user_pends_addition_of_course(step, course_name, category_name):
    with app.test_request_context():
        category = Category.get_single(category_name=category_name, language=aloe.world.language)
        course = Course.get_single(course_name=course_name, language=aloe.world.language)
        aloe.world.response = aloe.world.app.post(
            "/category/editcourses/" + str(category.category_id),
            data={
                "courses[]": category.course_ids() + [course.course_id],
            }
        )

@aloe.step(u'the user pends translation \"([\w\d ]*)\" in \"([\w\d ]*)\" for course \"([\w\d ]*)\"')
def the_translation_in_language_is_pending_to_be_added_to_course(step, course_name_translation, language, course_name_en):
    with app.test_request_context():
        course = Course.get_single(course_name=course_name_en, language="en")
        aloe.world.response = aloe.world.app.post(
            "/course/edit/" + str(course.course_id),
            data={
                fieldname_with_language("course_name", language): course_name_translation,
                "languages": [language]
            }
        )
