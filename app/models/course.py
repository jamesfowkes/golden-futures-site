import logging

from functools import total_ordering

import json

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

from app.models.university_course_map import university_course_map_table
from app.models.university_course_map import university_course_pending_map_table

from app.models.category_course_map import category_course_map_table
from app.models.category_course_map import category_course_pending_map_table

from app.models.category import CategoryPending

logger = logging.getLogger(__name__)

class CourseBase():

    def __init__(self, course_name, language=None):
        self.set_name(course_name, language)

    def set_name(self, course_name, language=None):
        if language:
            self.translations[language].course_name = course_name
        else:
            self.current_translation.course_name = course_name

    def add_to_category(self, category_id):
        category = CategoryPending.get_single(category_id=category_id)
        self.categories.append(category)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<ID: {}, Names: '{}', Categories: '{}'>".format(
            self.course_id,
            ", ".join(["{} ({})".format(translation.course_name, lang) for lang, translation in self.translations.items()]),
            ", ".join([str(c.category_name) for c in self.categories])
        )

    def __eq__(self, other):
        return self.course_name == other.course_name

    def __ne__(self, other):
        return self.course_name != other.course_name

    def __lt__(self, other):
        return self.course_name < other.course_name

    def json(self):
        return {
            "course_name": self.course_name,
            "category_name": ", ".join([c.category_name for c in self.categories])
        }

    def university_names(self):
        return [uni.university_name for uni in self.universities]
        
    @classmethod
    def create(cls, course_name, language, category_id=None):
        logger.info("Creating course %s (%s)", course_name, language)
        course = cls(course_name, language)
        db.session.add(course)
        db.session.commit()
        if category_id:
            course.add_to_category(category_id)
        return course

    @classmethod
    def get_by_name(cls, course_name):
        return db.session.query(cls).filter_by(course_name=course_name).all()

    @classmethod
    def get_single_by_id(cls, course_id):
        try:
            return db.session.query(cls).filter_by(course_id=course_id).one()
        except:
            return None

@total_ordering
class Course(CourseBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Course"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universities = db.relationship('University', secondary=university_course_map_table, back_populates="courses")
    categories = db.relationship('Category', secondary=category_course_map_table, back_populates="courses")

class CourseTranslation(translation_base(Course)):
    __tablename__ = 'CourseTranslation'
    course_name = sa.Column(sa.Unicode(80))

class CoursePending(CourseBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "CoursePending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universities = db.relationship('UniversityPending', secondary=university_course_pending_map_table, back_populates="courses")
    categories = db.relationship('CategoryPending', secondary=category_course_pending_map_table, back_populates="courses")

class CoursePendingTranslation(translation_base(CoursePending)):
    __tablename__ = 'CoursePendingTranslation'
    course_name = sa.Column(sa.Unicode(80))
