import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class Facility(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Facility"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    facility_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="facilities")

    def __init__(self, university_id, facility, language):
        self.university_id = university_id
        self.add_translation(facility, language)

    def add_translation(self, facility, language=None):
        if language:
            self.translations[language].facility_string = facility
        else:
            self.current_translation.facility_string = facility

    @classmethod
    def create(cls, university_id, facility, language=None):
        university_id = int(university_id)
        facility_obj = cls(university_id, facility, language)
        db.session.add(facility_obj)
        db.session.commit()
        return facility_obj

    def json(self):
        return {
            "facility_id": self.facility_id, 
            "university_name": self.university.university_name,
            "facility": self.current_translation.facility_string
        }

class FacilityTranslation(translation_base(Facility)):
    __tablename__ = 'FacilityTranslation'
    facility_string = sa.Column(sa.Unicode(80))
    unique_facility_constraint = sa.PrimaryKeyConstraint('id', 'facility_string', 'locale', name='ufc_1')
