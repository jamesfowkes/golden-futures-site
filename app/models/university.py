import os
import shutil
import logging
import random
import string

from pathlib import Path

import json
from werkzeug.datastructures import MultiDict

from flask import g, url_for

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app import app, APP_PATH
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

THIS_PATH = Path(__file__).parent

def get_images_path():
    return Path("app", app.config["IMAGES_PATH"][0]).resolve()

def get_random_filename(ext = ".tmp"):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)) + ext

class UniversityBase():
    def __init__(self, translations):
        logger.info("Creating university %s", translations["en"]["university_name"])
        self.set_translations(translations)

    @staticmethod
    def json_skeleton():
        return {
            "university_id": -1,
            "latlong": "",
            "web_address": "",
            "courses" : [],
            "facilities" : [],
            "contact_details": [],
            "admissions": [],
            "tuition_fees": [],
            "scholarships" : [],
            "quotes" : [],
            "translations": {}
        }

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.university_id, self.university_name)

    def __eq__(self, other):
        return self.current_translation.university_name == other.current_translation.university_name

    def __ne__(self, other):
        return self.current_translation.university_name != other.current_translation.university_name

    def __lt__(self, other):
        return self.current_translation.university_name < other.current_translation.university_name

    def json(self):
        return {
            "university_id": self.university_id,
            "latlong": self.latlong or "",
            "web_address": self.web_address or "",           
            "courses" : [c.json() for c in self.courses],
            "facilities" : [f.json() for f in self.facilities],
            "contact_details": [c.json() for c in self.contact_details],
            "admissions": [a.json() for a in self.admissions],
            "tuition_fees": [t.json() for t in self.tuition_fees],
            "scholarships" : [s.json() for s in self.scholarships],
            "quotes" : [s.json() for s in self.quotes],
            "translations": self.all_translations()
        }
    
    def request_dict(self):
        data = MultiDict()
        data["university_latlong"] = self.latlong or ""
        data["university_web_address"] = self.web_address or ""
        data.setlist("courses[]", [str(c.course_id) for c in self.courses])

        for index, tf in enumerate(self.tuition_fees):
            for lang in app.config["SUPPORTED_LOCALES"]:
                data["tuition_fee_award[{}]".format(lang)].add(tf.tuition_fee_award)
                data["tuition_fee_period[{}]".format(lang)].add(tf.tuition_fee_period)
            data["tuition_fee_min"].add(str(tf.tuition_fee_min))
            data["tuition_fee_max"].add(str(tf.tuition_fee_max))
            data["tuition_fee_currency"].add(tf.tuition_fee_currency)

            if tf.include_in_filter:
                data["tuition_fee_include_in_filter"].add(str(index))

        for lang in app.config["SUPPORTED_LOCALES"]:

            data["university_name[{}]".format(lang)] = self.translations[lang].university_name or ''
            data["university_intro[{}]".format(lang)] = self.translations[lang].university_intro or ''

            for f in self.facilities:
                data["university_facility[{}]".format(lang)].add(f.translations[lang].facility_string)

            for cd in self.contact_details:
                data["university_contact_detail[{}]".format(lang)].add(cd.translations[lang].contact_detail_string)

            for a in self.admissions:
                data["admission[{}]".format(lang)].add(a.translations[lang].admission_string)

            for s in self.scholarships:
                data["university_scholarship[{}]".format(lang)].add(a.translations[lang].scholarship_string)

            for q in self.quotes:
                data["university_quotes[{}]".format(lang)].add(q.translations[lang].quote_string)

        data["languages"] = ",".join(app.config["SUPPORTED_LOCALES"])

        return data

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

    def has_course(self, course):
        if type(course) == Course:
            return course.course_id in [course.course_id for course in self.courses]
        else:
            return course in [course.course_id for course in self.courses]

    def add_courses(self, courses):
        for c in courses:
            self.add_course(c)
        
    def set_courses(self, courses):
        self.remove_courses()
        self.add_courses(courses)

    def remove_tuition_fees(self):
        for tuition_fee in self.tuition_fees:
            tuition_fee.delete()

    def add_tuition_fees(self, tuition_fees):
        for c in tuition_fees:
            self.add_tuition_fee(c)
        
    def add_tuition_fee(self, tuition_fee):
        self.tuition_fees.append(tuition_fee)
        self.save()

    def remove_contact_details(self):
        for contact_detail in self.contact_details:
            contact_detail.delete()
        self.save()

    def remove_scholarships(self):
        for scholarship in self.scholarships:
            scholarship.delete()
        self.save()

    def remove_facilities(self):
        for facility in self.facilities:
            facility.delete()
        self.save()

    def remove_admissions(self):
        for admission in self.admissions:
            admission.delete()
        self.save()

    def remove_quotes(self):
        for quote in self.quotes:
            quote.delete()
        self.save()

    def set_latlong(self, latlong):
        self.latlong = latlong
        self.save()

    def set_web_address(self, web_address):
        self.web_address = web_address
        self.save()

    def get_img_data(self, img_path):
        img_path = Path(img_path)
        return {
            "name":img_path.name,
            "full_url": url_for("images", filename=str(img_path.name), width=app.config["IMAGE_WIDTH"], mode="fit"),
            "thumb_url": url_for(
                "images",
                filename=str(img_path.name),
                width=app.config["THUMB_SIZE"], height=app.config["THUMB_SIZE"], mode="crop"),
            "size": img_path.stat().st_size
        }

    def ensure_pending_folder(self):
        self.pending_images_path.mkdir(exist_ok=True)

    def images(self):
        paths = sorted([f for f in get_images_path().glob("{}_*".format(self.university_id)) if f.is_file()])
        return [self.get_img_data(p) for p in paths]

    @property
    def images_path(self):
        return get_images_path()

    @property
    def pending_images_path(self):
        return get_images_path().joinpath("pending", str(self.university_id))

    def get_image_path(self, folder_path, existing_path, index):
        new_name = "{}_{:02d}{}".format(self.university_id, index, existing_path.suffix)
        return folder_path.joinpath(new_name)

    def get_pending_image_path(self, existing_path, index):
        new_name = "{}_{:02d}{}".format(self.university_id, index, existing_path.suffix)
        return self.pending_images_path.joinpath(new_name)

    def pend_new_image(self, image_file):
        self.ensure_pending_folder()
        logger.info("Saving {} for {}".format(image_file.filename, self.university_name))
        image_file.save(self.pending_images_path.joinpath(image_file.filename).as_posix())

    def pend_existing_image(self, existing_filename):
        self.ensure_pending_folder()
        existing_file = self.images_path.joinpath(existing_filename)
        if existing_file.is_file():
            logger.info("Copying {} to pending".format(existing_filename))
            result = {"success" : True}
            new_file = self.pending_images_path.joinpath(existing_filename)
            shutil.copy(str(existing_file), str(new_file))
        else:
            logger.info("Could not find {} for pending".format(existing_file.as_posix()))
            result = {"success" : False}

    def clear_pending_images(self):
        self.ensure_pending_folder()
        logger.info("Clearing images from {}".format(self.pending_images_path))
        for f in self.pending_images_path.glob("*"):
            f.unlink();

    def rename_pending_image(self, old_filename, new_filename):
        self.ensure_pending_folder()
        new_path = self.pending_images_path.joinpath(new_filename)
        existing_path = self.pending_images_path.joinpath(old_filename)
        existing_path.replace(new_path)

    def index_pending_image(self, filename, index):
        self.ensure_pending_folder()
        new_path = self.get_image_path(self.pending_images_path, Path(filename), index)
        existing_path = self.pending_images_path.joinpath(filename)
        logger.info("Renaming {} to {}".format(filename, new_path.name))
        existing_path.replace(new_path)

    def order_pending_images(self, original_filenames):
        self.ensure_pending_folder()
        temporary_filenames = []
        for i, f in enumerate(original_filenames):
            temp = "{}_{}".format(i, get_random_filename(Path(f).suffix))
            temporary_filenames.append(temp)
            self.rename_pending_image(f, temp)

        for i, f in enumerate(temporary_filenames):
            self.index_pending_image(f, i)

    @property
    def lat(self):
        try:
            return self.latlong.split(",")[0]
        except AttributeError:
            return None

    @property
    def long(self):
        try:
            return self.latlong.split(",")[1]
        except AttributeError:
            return None

    @classmethod
    def create(cls, translations):
        university = cls(translations)
        university.save()
        return university

    @classmethod
    def get_by_name(cls, university_name, language=None):
        return cls.get_single_with_language(language, university_name=university_name)

    @classmethod
    def get_single_by_id(cls, university_id, except_on_no_result=False):
        return cls.get_single(university_id=university_id, except_on_no_result=except_on_no_result)

class University(UniversityBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "University"
    __translatable__ = {'locales': app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    university_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latlong = db.Column(db.String)
    web_address = db.Column(db.String)
    courses = db.relationship('Course', secondary=university_course_map_table, back_populates="universities")
    facilities = db.relationship("Facility", back_populates="university")
    contact_details = db.relationship("ContactDetail", back_populates="university")
    admissions = db.relationship("Admission", back_populates="university")
    tuition_fees = db.relationship("TuitionFee", back_populates="university")
    scholarships = db.relationship("Scholarship", back_populates="university")
    quotes = db.relationship("Quote", back_populates="university")
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

    def is_pending(self):
        return False

    def add_course(self, course):
        self.courses.append(course)
        self.save()

    def remove_courses(self):
        for course in self.courses:
            self.courses.remove(course)
    
        self.save()

    def is_pending(self):
        return False

class UniversityTranslation(translation_base(University)):
    __tablename__ = 'UniversityTranslation'
    university_name = sa.Column(sa.Unicode(80))
    university_intro = sa.Column(sa.Unicode())

class UniversityPending(UniversityBase, PendingChangeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "UniversityPending"
    __translatable__ = {'locales': app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey("University.university_id"), unique=True, nullable=True)
    pending_type = db.Column(db.String(6), nullable=False)

    latlong = db.Column(db.String)
    web_address = db.Column(db.String)

    pending_courses = db.relationship('UniversityPendingCourse', back_populates="university")
    facilities = db.relationship("FacilityPending", back_populates="university")
    contact_details = db.relationship("ContactDetailPending", back_populates="university")
    admissions = db.relationship("AdmissionPending", back_populates="university")
    tuition_fees = db.relationship("TuitionFeePending", back_populates="university")
    scholarships = db.relationship("ScholarshipPending", back_populates="university")
    quotes = db.relationship("QuotePending", back_populates="university")
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
        super(BaseModelTranslateable,self).delete()

    def approve(self):
        if self.is_addition():
            logger.info("Adding university %s", self.translations["en"].university_name)
            new_university = University.create(self.all_translations())
            self.approve_detail_changes(new_university)
            new_university.save()

        elif self.is_edit():
            university = University.get(university_id=self.university_id).one();
            logger.info("Editing university %s", university.translations["en"].university_name)
            self.approve_detail_changes(university)
            university.set_translations(self)
            university.save()

        elif self.is_deletion():
            university = University.get(university_id=self.university_id).one();
            logger.info("Deleting university %s", university.translations["en"].university_name)
            university.delete()

        self._delete()

    def approve_detail_changes(self, university):

        logger.info("Approving detail changes... ")

        logger.info("New latlong: %s", self.latlong)
        
        university.latlong = self.latlong
        
        university.remove_facilities()
        for facility in self.facilities:
            facility.approve(university.university_id)
        
        university.remove_contact_details()
        for contact_detail in self.contact_details:
            contact_detail.approve(university.university_id)

        university.remove_admissions()
        for admission in self.admissions:
            admission.approve(university.university_id)

        university.remove_tuition_fees()
        for tuition_fee in self.tuition_fees:
            tuition_fee.approve(university.university_id)

        university.remove_scholarships()
        for scholarship in self.scholarships:
            scholarship.approve(university.university_id)

        university.remove_quotes()
        for quote in self.quotes:
            quote.approve(university.university_id)

        university.remove_courses()
        for course in self.pending_courses:
            university.courses.append(Course.get_single(course_id=course.course_id))
            course.delete()

        logger.info("Detail changes done.")

    def reject(self):
        for facility in self.facilities:
            facility.reject()
        
        for contact_detail in self.contact_details:
            contact_detail.reject()

        for admission in self.admissions:
            admission.reject()

        for tuition_fee in self.tuition_fees:
            tuition_fee.reject()

        for scholarship in self.scholarships:
            scholarship.reject()

        for quote in self.quotes:
            quote.reject()
        
        for course in self.pending_courses:
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
       
    def remove_courses(self):
        for course in self.pending_courses:
            course.delete()

    @property
    def course_names(self):
        names = [c.course_name for c in self.pending_courses]
        return sorted(names)

    def facility_names(self):
        names = [f.facility_string for f in self.facilities]
        return sorted(names)

    def categories(self):
        categories = []
        for pending_course in self.courses:
            categories.extend(Course.get_single(course_id=pending_course.course_id).categories)

        return set(categories)

    def images(self):
        paths = sorted([f for f in self.pending_images_path.glob("*") if f.is_file()])
        logger.info(paths)
        return [self.get_img_data(p) for p in paths]

    def get_img_data(self, img_path):
        img_path = Path(img_path)
        return {
            "name":img_path.name,
            "full_url": url_for("images", filename=str(Path("pending", str(self.university_id), img_path.name)), width=app.config["IMAGE_WIDTH"], mode="fit"),
            "thumb_url": url_for(
                "images",
                filename=str(img_path.name),
                width=app.config["THUMB_SIZE"], height=app.config["THUMB_SIZE"], mode="crop"),
            "size": img_path.stat().st_size
        }

    def is_pending(self):
        return True

    def is_addition(self):
        return self.is_add_edit() and self.university_id is None

    def is_edit(self):
        return self.is_add_edit() and self.university_id is not None

    def is_add_edit(self):
        return self.pending_type == "add_edit"

    def is_deletion(self):
        return self.pending_type == "del"

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

    @classmethod
    def get_single_by_id(cls, pending_id, except_on_no_result=False):
        return cls.get_single(pending_id=pending_id, except_on_no_result=except_on_no_result)

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
