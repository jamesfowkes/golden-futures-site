import logging

from functools import total_ordering

import json

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import PendingChangeBase, BaseModelTranslateable, DeclarativeBase, DbIntegrityException

from app.models.university_course_map import university_course_map_table

from app.models.category_course_map import category_course_map_table

from app.models.pending_changes import PendingChanges

logger = logging.getLogger(__name__)

class CourseBase():

    def __init__(self, course_name, language=None):
        self.set_name(course_name, language)

    def set_name(self, course_name, language=None):
        if language:
            self.translations[language].course_name = course_name
        else:
            self.current_translation.course_name = course_name

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
    def create(cls, course_name, language):
        logger.info("Creating course %s (%s)", course_name, language)
        course = cls(course_name, language)
        db.session.add(course)
        db.session.commit()
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
        for lang in app.app.config["SUPPORTED_LOCALES"]:
            self.translations[lang].course_name = other.translations[lang].course_name

        db.session.add(self)
        db.session.commit()

    def is_pending(self):
        return False

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

class CoursePending(CourseBase, PendingChangeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "CoursePending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("Course.course_id"), unique=True, nullable=True)
    pending_type = db.Column(db.String(6), nullable=False)
    
    course = db.relationship('Course', uselist=False)

    def __init__(self, course_name, language, pending_type):
        
        self.pending_type = pending_type
        CourseBase.__init__(self, course_name, language)
        
        try:
            db.session.add(self)
            db.session.commit()
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
            "course_name": self.current_translation.course_name,
            "pending": self.pending_type
        }

    def approve(self):
        if self.pending_type == "add_edit":
            if self.course_id is None:
                logger.info("Adding course %s", self.translations["en"].course_name)
                new_course = Course.create(self.translations["en"].course_name, "en")
                for lang, translation in self.translations.items():
                    new_course.translations[lang].course_name = translation.course_name
                db.session.add(new_course)
                db.session.commit()
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
        
    def is_pending(self):
        return True

    @classmethod
    def create_from(cls, existing_course, pending_type):
        new = cls("", "en", pending_type)
        new.update(existing_course)
        return new

    @classmethod
    def addition(cls, course_name, language):
        pending = cls(course_name, language, "add_edit")
        return pending

    @classmethod
    def edit(cls, existing_course):
        try:
            pending = cls.create_from(existing_course, "add_edit")

        except DbIntegrityException:
            pending = cls.get_single(course_id = existing_course.course_id)

        return pending

    @classmethod
    def deletion(cls, existing_course):
        pending = cls.create_from(existing_course, "del")
        return pending

class CoursePendingTranslation(translation_base(CoursePending)):
    __tablename__ = 'CoursePendingTranslation'
    course_name = sa.Column(sa.Unicode(80))
    old_name = sa.Column(sa.Unicode(80))
