import logging

import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModel, BaseModelTranslateable, DeclarativeBase, PendingChangeBase, DbIntegrityException, TranslationMixin, get_locales

from app.models.facility import Facility
from app.models.contact_detail import ContactDetail
from app.models.admission import Admission
from app.models.tuition_fee import TuitionFee
from app.models.scholarship import Scholarship

from app.models.course import Course

from app.models.university_course_map import university_course_map_table

from app.models.pending_changes import PendingChanges

logger = logging.getLogger(__name__)

class UniversityBase():
    def __init__(self, translations):
        logger.info("Creating university %s", translations["en"]["university_name"])
        self.set_translations(translations)

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
    
    def set_translations(self, translation_dict_or_uni_obj):
        try:
            translations = translation_dict_or_uni_obj.all_translations()
        except:
            translations = translation_dict_or_uni_obj

        for language in get_locales(translations):
            if "university_name" in translations[language]:
                self.translations[language].university_name = translations[language]["university_name"]
            if "university_intro" in translations[language]:
                self.translations[language].university_intro = translations[language]["university_intro"]

    def maximum_fee(self):
        return max([fee.tuition_fee_max for fee in self.tuition_fees if fee.include_in_filter])

    def minimum_fee(self):
        return min([fee.tuition_fee_min for fee in self.tuition_fees if fee.include_in_filter])

    def course_names(self):
        names = [c.course_name for c in self.courses]
        return sorted(names)

    def facility_names(self):
        names = [f.facility_string for f in self.facilities]
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

    @classmethod
    def create(cls, translations):
        university = cls(translations)
        university.save()
        return university

    @classmethod
    def get_by_name(cls, university_name, language=None):
        return cls.get_single_with_language(language, university_name=university_name)

    @classmethod
    def get_single_by_id(cls, university_id):
        return cls.get_single(university_id=university_id)

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
    pendingedit = db.relationship("UniversityPending", back_populates="university")
    
    def get_contact_detail(self, contact_detail_string):
        for contact_detail in self.contact_details:
            if contact_detail.contact_detail_string == contact_detail_string:
                return contact_detail
        return None

    def get_admission(self, admission_string):
        for admission in self.admissions:
            if admission.admission_string == admission_string:
                return admission
        return None

    def add_course(self, course):
        self.courses.append(course)
        self.save()

class UniversityTranslation(translation_base(University)):
    __tablename__ = 'UniversityTranslation'
    university_name = sa.Column(sa.Unicode(80))
    university_intro = sa.Column(sa.Unicode())

class UniversityPending(UniversityBase, PendingChangeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "UniversityPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey("University.university_id"), unique=True, nullable=True)
    pending_type = db.Column(db.String(6), nullable=False)

    pending_courses = db.relationship('UniversityPendingCourse', back_populates="university")
    facilities = db.relationship("FacilityPending", back_populates="university")
    contact_details = db.relationship("ContactDetailPending", back_populates="university")
    admissions = db.relationship("AdmissionPending", back_populates="university")
    tuition_fees = db.relationship("TuitionFeePending", back_populates="university")
    scholarships = db.relationship("ScholarshipPending", back_populates="university")
    university = db.relationship("University", back_populates="pendingedit")

    def __init__(self, translations, pending_type, university_id=None):
        self.pending_type = pending_type
        self.university_id = university_id
        UniversityBase.__init__(self, translations)
                
        try:
            self.save()
        except sa.exc.IntegrityError:
            raise DbIntegrityException()

    @property
    def courses(self):
        return [Course.get_single(course_id = c.course_id) for c in self.pending_courses]
    
    def _delete(self):
        for lang, translation in self.translations:
            db.session.delete(translation)

        for facility in self.facilities:
            facility.delete()

        for course in self.pending_courses:
            course.delete()

        super(BaseModelTranslateable,self).delete()

    def approve(self):
        if self.pending_type == "add_edit":
            if self.university_id is None:
                logger.info("Adding university %s", self.translations["en"].university_name)

                new_university = University.create(self.all_translations())

                for facility in self.facilities:
                    facility.approve(new_university.university_id)
                    
                for contact_detail in self.contact_details:
                    contact_detail.approve(new_university.university_id)

                for admission in self.admissions:
                    admission.approve(new_university.university_id)

                for tuition_fee in self.tuition_fees:
                    tuition_fee.approve(new_university.university_id)

                for scholarship in self.scholarships:
                    scholarship.approve(new_university.university_id)

                for course_to_add in self.pending_courses:
                    new_university.courses.append(Course.get_single(course_id=course_to_add.course_id))

            else:
                university = University.get(university_id=self.university_id).one();
                logger.info("Editing university %s", university.translations["en"].university_name)
                university.set_translations(self)
                university.save()

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
        pending_course = UniversityPendingCourse(university_id=self.university_id, course_id=course.course_id)
        self.pending_courses.append(pending_course)
        self.save()

    def remove_course(self, course):
        pending_course = UniversityPendingCourse.get(university_id=self.university_id, course_id=course.course_id)
        pending_course.delete()
        self.save()

    @property
    def course_names(self):
        names = [c.course_name for c in self.pending_courses]
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
        new_university = cls(existing_university.all_translations(), pending_type, existing_university.university_id)
        new_university.save()
        return new_university

    @classmethod
    def addition(cls, university_name):
        pending = cls(university_name, "add_edit")
        pending.save()
        return pending

    @classmethod
    def edit(cls, existing_university):
        pending = cls.create_from(existing_university, "add_edit")
        return pending

    @classmethod
    def deletion(cls, existing_university):
        pending = cls.create_from(existing_university, "del")
        return pending

class UniversityPendingTranslation(translation_base(UniversityPending), TranslationMixin):
    __tablename__ = 'UniversityPendingTranslation'
    university_name = sa.Column(sa.Unicode(80), unique=True)
    university_intro = sa.Column(sa.Unicode())

class UniversityPendingCourse(BaseModel, DeclarativeBase):

    __tablename__ = "UniversityPendingCourse"
    university_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'), nullable=False, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False, primary_key=True)
    university = db.relationship('UniversityPending', back_populates="pending_courses")

    @property
    def course_name(self):
        return Course.get_single(course_id=self.course_id).course_name
