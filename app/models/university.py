import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModelTranslateable, DeclarativeBase

import app.models.facility
import app.models.contact_detail
import app.models.admission
import app.models.tuition_fee

from app.models.university_course_map import university_course_map_table

class University(Translatable, BaseModelTranslateable, DeclarativeBase):

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
    
    def add_translated_name(self, university_name):
        self.current_translation.university_name = university_name
        db.session.commit()
        
    @classmethod
    def create(cls, university_name, language=None):
        university = cls(university_name, language)
        db.session.add(university)
        db.session.commit()
        return university

    @classmethod
    def get_by_name(cls, university_name, language=None):
        return cls.get_single(university_name=university_name, language=language)

    @classmethod
    def get_single_by_id(cls, university_id):
        return cls.get_single(university_id=university_id)

    def add_course(self, course):
        self.courses.append(course)
        db.session.add(self)
        db.session.commit()

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

class UniversityTranslation(translation_base(University)):
    __tablename__ = 'UniversityTranslation'
    university_name = sa.Column(sa.Unicode(80))
    university_intro = sa.Column(sa.Unicode())