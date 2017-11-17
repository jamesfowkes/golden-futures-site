import logging

import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModel, BaseModelTranslateable, DeclarativeBase, PendingChangeBase, DbIntegrityException

import app.models.facility
import app.models.contact_detail
import app.models.admission
import app.models.tuition_fee

from app.models.course import Course

from app.models.university_course_map import university_course_map_table

from app.models.pending_changes import PendingChanges

logger = logging.getLogger(__name__)

class UniversityBase():
    def __init__(self, university_name, language):
        self.translations[language].university_name = university_name

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.university_id, self.university_name)

    def __eq__(self, other):
        return self.current_translation.university_name == other.current_translation.university_name

    def __ne__(self, other):
        return self.current_translation.university_name != other.current_translation.university_name

    def __lt__(self, other):
        return self.current_translation.university_name < other.current_translation.university_name

    def json(self):
        return {"university_id": self.university_id, "university_name": self.current_translation.university_name, "language": get_current_locale(self)}
    
    def add_translated_name(self, university_name, language=None):
        logger.info("Adding translation %s (%s) to university %s", university_name, language, self.translations["en"].university_name)
        if language:
            self.translations[language].university_name = university_name
        else:
            self.current_translation.university_name = university_name
        db.session.commit()

    def set_intro(self, intro, lang=None):
        if lang:
            self.translations[lang].university_intro = intro
        else:
            self.current_translation.university_intro = intro

        db.session.commit()
        
    @classmethod
    def create(cls, university_name, language=None):
        university = cls(university_name, language)
        db.session.add(university)
        db.session.commit()
        return university

    @classmethod
    def get_by_name(cls, university_name, language=None):
        return cls.get_single_with_language(language, university_name=university_name)

    @classmethod
    def get_single_by_id(cls, university_id):
        return cls.get_single(university_id=university_id)

    def maximum_fee(self):
        return max([fee.tuition_fee_max for fee in self.tuition_fees])

    def minimum_fee(self):
        return min([fee.tuition_fee_min for fee in self.tuition_fees])

    def course_names(self):
        names = [c.course_name for c in self.courses]
        return sorted(names)

    def categories(self):
        categories = []
        for course in self.courses:
            categories.extend(course.categories)

        return set(categories)

    def courses_by_category(self):
        category_course_map = {}
        for category in self.categories():
            category_course_map[category] = [course for course in category.courses if course in self.courses]

        return category_course_map

class University(UniversityBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "University"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    university_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    courses = db.relationship('Course', secondary=university_course_map_table, back_populates="universities")
    facilities = db.relationship("Facility", back_populates="university")
    contact_details = db.relationship("ContactDetail", back_populates="university")
    admissions = db.relationship("Admission", back_populates="university")
    tuition_fees = db.relationship("TuitionFee", back_populates="university")
    scholarships = db.relationship("Scholarship", back_populates="university")
        
    def add_course(self, course):
        self.courses.append(course)
        db.session.add(self)
        db.session.commit()

class UniversityTranslation(translation_base(University)):
    __tablename__ = 'UniversityTranslation'
    university_name = sa.Column(sa.Unicode(80))
    university_intro = sa.Column(sa.Unicode())

class UniversityPending(UniversityBase, PendingChangeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "UniversityPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, unique=True, nullable=True)
    pending_type = db.Column(db.String(6), nullable=False)

    pending_courses = db.relationship('UniversityPendingCourses', back_populates="university")
    facilities = db.relationship("FacilityPending", back_populates="university")
    contact_details = db.relationship("ContactDetailPending", back_populates="university")
    admissions = db.relationship("AdmissionPending", back_populates="university")
    tuition_fees = db.relationship("TuitionFeePending", back_populates="university", foreign_key="TuitionFeePending.university_id")
    scholarships = db.relationship("ScholarshipPending", back_populates="university")

    def __init__(self, university_name, language, pending_type):
        UniversityBase.__init__(self, university_name, language)
        self.pending_type = pending_type
        
        try:
            db.session.add(self)
            db.session.commit()
        except sa.exc.IntegrityError:
            raise DbIntegrityException()

    @property
    def courses(self):
        return [Course.get_single(course_id = c.course_id) for c in self.pending_courses]
    
    def _delete(self):
        for lang, translation in self.translations:
            db.session.delete(translation)

        for course in self.courses:
            course.delete()

        super(BaseModelTranslateable,self).delete()

    def approve(self):
        if self.pending_type == "add_edit":
            if self.university_id is None:
                logger.info("Adding university %s", self.translations["en"].university_name)
                new_university = University.create(self.translations["en"].university_name, "en")
                new_university.set_intro(self.translations["en"].university_intro, "en")

                for course in self.courses:
                    new_university.add_course(Course.get_single(course_id=course.course_id))
            else:
                university = University.get(university_id=self.university_id).one();
                logger.info("Editing university %s", university.translations["en"].university_name)
                university.update(self)
        elif self.pending_type == "del":
            university = University.get(university_id=self.university_id).one();
            logger.info("Deleting university %s", university.translations["en"].university_name)
            university.delete()

        self._delete()

    def reject(self):
        for course in self.courses:
            course.delete()
        self._delete()

    def add_course(self, course):
        self.courses.append(UniversityPendingCourses(university_id=self.university_id, course_id=course.course_id))
        db.session.add(self)
        db.session.commit()

    def course_names(self):
        names = [Course.get_single(course_id=c.course_id).course_name for c in self.courses]
        return sorted(names)

    def categories(self):
        categories = []
        for pending_course in self.courses:
            categories.extend(Course.get_single(course_id=pending_course.course_id).categories)

        return set(categories)

    def is_pending(self):
        return True

    def is_addition(self):
        return self.university_id is None

    @classmethod
    def create_from(cls, existing_university, pending_type):
        new = cls("", "en", pending_type)
        new.update(existing_university)
        return new

    @classmethod
    def addition(cls, university_name, language):
        pending = cls(university_name, language, "add_edit")
        return pending

    @classmethod
    def edit(cls, existing_university):
        pending = cls.create_from(existing_university, "add_edit")
        pending.pending_type = "add_edit"
        return pending

    @classmethod
    def deletion(cls, existing_university):
        pending = cls.create_from(existing_university, "del")
        pending.pending_type = "del"
        return pending

class UniversityPendingTranslation(translation_base(UniversityPending)):
    __tablename__ = 'UniversityPendingTranslation'
    university_name = sa.Column(sa.Unicode(80), unique=True)
    university_intro = sa.Column(sa.Unicode())

class UniversityPendingCourses(BaseModel, DeclarativeBase):

    __tablename__ = "UniversityPendingCourses"
    university_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'), nullable=False, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False, primary_key=True)
    university = db.relationship('UniversityPending', back_populates="pending_courses")
