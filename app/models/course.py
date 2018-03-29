import logging

from functools import total_ordering

import json

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import PendingChangeBase, BaseModelTranslateable, DeclarativeBase, DbIntegrityException
from app.models.base_model import get_locales, get_translation

from app.models.university_course_map import university_course_map_table

from app.models.category_course_map import category_course_map_table

from app.models.pending_changes import PendingChanges

logger = logging.getLogger(__name__)

class CourseBase():

    def __init__(self, translations):
        self.set_translations(translations)

    def set_name(self, course_name, language=None):
        if language:
            self.translations[language].course_name = course_name
        else:
            self.current_translation.course_name = course_name
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
            "course_id": self.course_id,
            "translations": self.all_translations()
        }

    def university_names(self):
        return [uni.university_name for uni in self.universities]
        
    @classmethod
    def create(cls, translations):
        course = cls(translations)
        course.save()
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

    def update(self, other):
        self.course_id = other.course_id
        self.set_translations(other.translations)
        #for lang in app.app.config["SUPPORTED_LOCALES"]:
        #    self.translations[lang].course_name = other.translations[lang].course_name

        self.save()

    def is_pending(self):
        return False

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.set_translation(translations, language, "course_name")

@total_ordering
class Course(CourseBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Course"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universities = db.relationship('University', secondary=university_course_map_table, back_populates="courses")
    categories = db.relationship('Category', secondary=category_course_map_table, back_populates="courses")
    pending_change = db.relationship("CoursePending", uselist=False, back_populates="course")

class CourseTranslation(translation_base(Course)):
    __tablename__ = 'CourseTranslation'
    course_name = sa.Column(sa.Unicode(80))

class CoursePending(CourseBase, PendingChangeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "CoursePending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("Course.course_id"), unique=True, nullable=True)
    pending_type = db.Column(db.String(6), nullable=False)
    
    course = db.relationship('Course', uselist=False, back_populates="pending_change")

    def __init__(self, translations, pending_type):
        
        CourseBase.__init__(self, translations)
        self.pending_type = pending_type

        try:
            self.save()
        except sa.exc.IntegrityError:
            raise DbIntegrityException()

    def __repr__(self):
        return "<ID: {}, Names: '{}', Type: {}>".format(
            self.course_id,
            ", ".join(["{} ({})".format(translation.course_name, lang) for lang, translation in self.translations.items()]),
            self.pending_type
        )

    def _delete(self):
        for lang, translation in self.translations:
            db.session.delete(translation)

        super(BaseModelTranslateable,self).delete()
        
    def json(self):
        return {
            "course_name": self.course_name,
            "category_names": [],
            "language": self.current_language(),
            "pending_type": self.pending_type,
            "pending_id": self.pending_id
        }

    def approve(self):
        if self.pending_type == "add_edit":
            if self.course_id is None:
                logger.info("Adding course %s", self.translations["en"].course_name)
                new_course = Course.create(self.translations)
                new_course.save()
            else:
                course = Course.get(course_id=self.course_id).one();
                logger.info("Editing course %s", course.translations["en"].course_name)
                course.update(self)

        elif self.pending_type == "del":
            course = Course.get(course_id=self.course_id).one();
            logger.info("Deleting course %s", course.translations["en"].course_name)
            course.delete()

        self._delete()

    def reject(self):
        self._delete()

    def is_addition(self):
        return self.course_id is None

    def is_edit(self):
        return self.course_id is not None and self.pending_type == "add_edit"

    def is_deletion(self):
        return self.pending_type == "del"

    def is_pending(self):
        return True

    @classmethod
    def create_from(cls, existing_course, pending_type):
        logger.info("Creating %s from %s", cls.__name__, existing_course.course_name)
        new = cls({}, pending_type)
        new.update(existing_course)
        return new

    @classmethod
    def addition(cls, translations):
        pending = cls(translations, "add_edit")
        return pending

    @classmethod
    def edit(cls, existing_course):
        if existing_course.pending_change:
            return existing_course.pending_change
        else:
            pending = cls.create_from(existing_course, "add_edit")

        return pending

    @classmethod
    def deletion(cls, existing_course):
        pending = cls.create_from(existing_course, "del")
        return pending

class CoursePendingTranslation(translation_base(CoursePending)):
    __tablename__ = 'CoursePendingTranslation'
    course_name = sa.Column(sa.Unicode(80), unique=True)

