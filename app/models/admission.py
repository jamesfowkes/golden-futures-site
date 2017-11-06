import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class AdmissionBase():

    def __init__(self, university_id, admission, language=None):
        self.university_id = university_id
        self.add_translated_admission(admission, language)

    def add_translated_admission(self, admission, language=None):
        if language:
            self.translations[language].admission_string = admission
        else:
            self.current_translation.admission_string = admission

    @classmethod
    def create(cls, university_id, admission, language=None):
        university_id = int(university_id)
        admission_obj = cls(university_id, admission, language)
        db.session.add(admission_obj)
        db.session.commit()
        return admission_obj

    def json(self):
        return {
            "admission_id": self.admission_id, 
            "university_name": self.university.university_name,
            "admission": self.current_translation.admission_string
        }

class Admission(AdmissionBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Admission"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    admission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="admissions")


class AdmissionTranslation(translation_base(Admission)):
    __tablename__ = 'AdmissionTranslation'
    admission_string = sa.Column(sa.Unicode(80))
    unique_admission_constraint = sa.PrimaryKeyConstraint('id', 'admission_string', 'locale', name='ufc_1')

class AdmissionPending(AdmissionBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "AdmissionPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    admission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.university_id'))
    university = db.relationship('UniversityPending', back_populates="admissions")

class AdmissionPendingTranslation(translation_base(AdmissionPending)):
    __tablename__ = 'AdmissionPendingTranslation'
    admission_string = sa.Column(sa.Unicode(80))
    unique_admission_constraint = sa.PrimaryKeyConstraint('id', 'admission_string', 'locale', name='ufc_1')