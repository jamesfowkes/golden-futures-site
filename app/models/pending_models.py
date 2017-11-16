
import logging

import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModelTranslateable, DeclarativeBase

from app.models.admission import AdmissionBase
from app.models.facility import FacilityBase
from app.models.scholarship import ScholarshipBase
from app.models.contact_detail import ContactDetailBase
from app.models.university import UniversityBase
from app.models.category import CategoryBase
from app.models.course import CourseBase
from app.models.tuition_fee import TuitionFeeBase

class Admission(AdmissionBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

    __tablename__ = "Admission"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    admission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="admissions")

class AdmissionTranslation(translation_base(Admission)):
    __bind_key__='pending'

    __tablename__ = 'AdmissionTranslation'
    admission_string = sa.Column(sa.Unicode(80))
    unique_admission_constraint = sa.PrimaryKeyConstraint('id', 'admission_string', 'locale', name='ufc_1')

class Facility(FacilityBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

    __tablename__ = "Facility"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    facility_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="facilities")

class FacilityTranslation(translation_base(Facility)):
    __bind_key__='pending'
    __tablename__ = 'FacilityTranslation'
    facility_string = sa.Column(sa.Unicode(80))
    unique_facility_constraint = sa.PrimaryKeyConstraint('id', 'facility_string', 'locale', name='ufc_1')

class Scholarship(ScholarshipBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

    __tablename__ = "Scholarship"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    scholarship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="scholarships")

class ScholarshipTranslation(translation_base(Scholarship)):
    __bind_key__='pending'
    __tablename__ = 'ScholarshipTranslation'
    scholarship_string = sa.Column(sa.Unicode(80))
    unique_scholarship_constraint = sa.PrimaryKeyConstraint('id', 'scholarship_string', 'locale', name='ufc_1')

class ContactDetail(ContactDetailBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

    __tablename__ = "ContactDetail"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    contact_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="contact_details")

class ContactDetailTranslation(translation_base(ContactDetail)):
    __bind_key__='pending'
    __tablename__ = 'ContactDetailTranslation'
    contact_detail_string = sa.Column(sa.Unicode(80))
    unique_contact_detail_constraint = sa.PrimaryKeyConstraint('id', 'contact_detail_string', 'locale', name='ufc_1')

class University(UniversityBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

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

class UniversityTranslation(translation_base(University)):
    __bind_key__='pending'
    __tablename__ = 'UniversityTranslation'
    university_name = sa.Column(sa.Unicode(80))
    university_intro = sa.Column(sa.Unicode())

class Category(CategoryBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

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
    __bind_key__='pending'
    __tablename__ = 'CategoryTranslation'
    category_name = sa.Column(sa.Unicode(80), unique=True)
    category_intro = sa.Column(sa.Unicode())
    category_careers = sa.Column(sa.Unicode())

class Course(CourseBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

    __tablename__ = "Course"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universities = db.relationship('University', secondary=university_course_map_table, back_populates="courses")
    categories = db.relationship('Category', secondary=category_course_map_table, back_populates="courses")

class CourseTranslation(translation_base(Course)):
    __bind_key__='pending'
    __tablename__ = 'CourseTranslation'
    course_name = sa.Column(sa.Unicode(80))

class TuitionFee(TuitionFeeBase, Translatable, BaseModelTranslateable, DeclarativeBase):
    __bind_key__='pending'

    __tablename__ = "TuitionFee"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="tuition_fees")

class TuitionFeeTranslation(translation_base(TuitionFee)):
    __bind_key__='pending'
    __tablename__ = 'TuitionFeeTranslation'
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))

