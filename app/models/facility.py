import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales

class FacilityBase():
    def __init__(self, university_id, translations):
        self.university_id = university_id
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.translations[language].facility_string = translations[language]["facility_string"]

    @classmethod
    def create(cls, university_id, translations):
        university_id = int(university_id)
        facility_obj = cls(university_id, translations)
        db.session.add(facility_obj)
        db.session.commit()
        return facility_obj

    def json(self):
        return {
            "facility_id": self.facility_id, 
            "university_name": self.university.university_name,
            "facility": self.current_translation.facility_string
        }

class Facility(FacilityBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Facility"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    facility_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="facilities")

class FacilityTranslation(translation_base(Facility)):
    __tablename__ = 'FacilityTranslation'
    facility_string = sa.Column(sa.Unicode(80))
    unique_facility_constraint = sa.PrimaryKeyConstraint('id', 'facility_string', 'locale', name='ufc_1')

class FacilityPending(FacilityBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "FacilityPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_facility_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('Facility.facility_id'), nullable=True)
    pending_uni_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship('UniversityPending', back_populates="facilities")
    pending_type = db.Column(db.String(6), nullable=False)

    def __init__(self, pending_uni_id, translations):
        self.pending_uni_id = pending_uni_id
        self.set_translations(translations)

    def approve(self, university_id):
        if self.pending_type == "add_edit":
            if self.facility_id:
                Facility.get_single(facility_id=self.facility_id).set_translations(self.translations)
            else:
                Facility.create(university_id, self.translations)

        self.delete()

    @classmethod
    def addition(cls, pending_uni_id, translations):
        facility_obj = cls(pending_uni_id, translations)
        facility_obj.pending_type = "add_edit"
        facility_obj.save()
        return facility_obj

    @classmethod
    def deletion(cls, facility):
        facility_obj = cls(facility.university.university_id, {})
        facility_obj.pending_type = "del"
        facility_obj.facility_id = facility.facility_id
        facility_obj.save()
        return facility_obj

class FacilityPendingTranslation(translation_base(FacilityPending), TranslationMixin):
    __tablename__ = 'FacilityPendingTranslation'
    facility_string = sa.Column(sa.Unicode(80))
    unique_facility_constraint = sa.PrimaryKeyConstraint('id', 'facility_string', 'locale', name='ufc_1')
