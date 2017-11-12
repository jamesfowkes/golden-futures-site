import logging

from functools import total_ordering

import json

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModel, BaseModelTranslateable, DeclarativeBase, PendingChangeBase, DbIntegrityException

from app.models.category_course_map import category_course_map_table
from app.models.course import Course
from app.models.pending_changes import PendingChanges

logger = logging.getLogger(__name__)

class CategoryBase():
    def __init__(self, category_name, language):
        logger.info("Creating base category %s (%s)", category_name, language)
        self.translations[language].category_name = category_name

    def __hash__(self):
        return self.category_id
    
    def __str__(self):    
        return self.current_translation.category_name

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.category_id, self.current_translation.category_name)

    def __eq__(self, other):
        return self.current_translation.category_name == other.current_translation.category_name

    def __ne__(self, other):
        return self.current_translation.category_name != other.current_translation.category_name

    def __lt__(self, other):
        return self.current_translation.category_name < other.current_translation.category_name

    def json(self):
        return {
            "category_name": self.current_translation.category_name,
            "language": get_current_locale(self)
            }

    def set_name(self, category_name, lang):
        self.translations[lang].category_name = category_name
        db.session.commit()

    def set_intro(self, intro, lang=None):
        if lang:
            self.translations[lang].category_intro = intro
        else:
            self.current_translation.category_intro = intro

        db.session.commit()

    def set_careers(self, careers, lang=None):
        if lang:
            self.translations[lang].category_careers = careers
        else:
            self.current_translation.category_careers = careers

        db.session.commit()

    @classmethod
    def create(cls, category_name, language):
        logger.info("Creating category %s (%s)", category_name, language)
        category = cls(category_name, language)
        
        db.session.add(category)
        db.session.commit()

        return category

    @classmethod
    def create_from(cls, existing_category):
        new = cls("","en")
        new.update(existing_category)
        return new

    def update(self, other):
        self.category_id = other.category_id
        for lang in app.app.config["SUPPORTED_LOCALES"]:
            self.translations[lang].category_name = other.translations[lang].category_name
            self.translations[lang].category_intro = other.translations[lang].category_intro
            self.translations[lang].category_careers = other.translations[lang].category_careers

        db.session.add(self)
        db.session.commit()

    def has_course(self, course):
        return course.course_id in [course.course_id for course in self.courses]
    
    def course_count(self):
        return len(self.courses)

@total_ordering
class Category(CategoryBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Category"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courses = db.relationship('Course', secondary=category_course_map_table, back_populates="categories")

    def add_course(self, course):
        self.courses.append(course)
        db.session.add(self)
        db.session.commit()

    def course_names(self):
        names = [c.course_name for c in self.courses]
        return sorted(names)

class CategoryTranslation(translation_base(Category)):
    __tablename__ = 'CategoryTranslation'
    category_name = sa.Column(sa.Unicode(80), unique=True)
    category_intro = sa.Column(sa.Unicode())
    category_careers = sa.Column(sa.Unicode())

class CategoryPending(CategoryBase, PendingChangeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "CategoryPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, unique=True, nullable=True)
    pending_type = db.Column(db.String(6), nullable=False)

    courses = db.relationship('CategoryPendingCourses', back_populates="category")

    def __init__(self, category_name, language, pending_type):
        self.pending_type = pending_type
        CategoryBase.__init__(self, category_name, language)
        try:
            db.session.add(self)
            db.session.commit()
        except sa.exc.IntegrityError:
            raise DbIntegrityException()

    def _delete(self):
        for lang, translation in self.translations:
            db.session.delete(translation)

        for course in self.courses:
            course.delete()

        super(BaseModelTranslateable,self).delete()

    def approve(self):
        if self.pending_type == "add":
            logger.info("Adding category %s", self.translations["en"].category_name)
            new_category = Category.create(self.translations["en"].category_name, "en")
            new_category.set_intro(self.translations["en"].category_intro, "en")
            new_category.set_careers(self.translations["en"].category_careers, "en")
        elif self.pending_type == "edit":
            category = Category.get(category_id=self.category_id).one();
            logger.info("Editing category %s", category.translations["en"].category_name)
            category.update(self)
        elif self.pending_type == "del":
            category = Category.get(category_id=self.category_id).one();
            logger.info("Deleting category %s", category.translations["en"].category_name)
            category.delete()

        self._delete()

    def reject(self):
        for course in self.courses:
            course.delete()
        self._delete()

    def add_course(self, course):
        self.courses.append(CategoryPendingCourses(category_id=self.category_id, course_id=course.course_id))
        db.session.add(self)
        db.session.commit()

    def course_names(self):
        names = [Course.get_single(course_id=c.course_id).course_name for c in self.courses]
        return sorted(names)

    @classmethod
    def all_by_type(cls):
        all_changes = cls.all();
        additions = [c for c in all_changes if c.pending_type == "add"]
        edits = [c for c in all_changes if c.pending_type == "edit"]
        dels = [c for c in all_changes if c.pending_type == "del"]

        return PendingChanges(additions, edits, dels)

    @classmethod
    def create_from(cls, existing_category, pending_type):
        new = cls("", "en", pending_type)
        new.update(existing_category)
        return new

    @classmethod
    def addition(cls, category_name, language):
        pending = cls(category_name, language, "add")
        return pending

    @classmethod
    def edit(cls, existing_category):
        pending = cls.create_from(existing_category, "edit")
        pending.pending_type = "edit"
        return pending

    @classmethod
    def deletion(cls, existing_category):
        pending = cls.create_from(existing_category, "del")
        pending.pending_type = "del"
        return pending

class CategoryPendingTranslation(translation_base(CategoryPending)):
    __tablename__ = 'CategoryPendingTranslation'
    category_name = sa.Column(sa.Unicode(80), unique=True)
    category_intro = sa.Column(sa.Unicode())
    category_careers = sa.Column(sa.Unicode())

class CategoryPendingCourses(BaseModel, DeclarativeBase):

    __tablename__ = "CategoryPendingCourses"
    category_id = db.Column(db.Integer, db.ForeignKey('CategoryPending.pending_id'), nullable=False, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False, primary_key=True)
    category = db.relationship('CategoryPending', back_populates="courses")