import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales
from app.models.pending_changes import pending_university_detail

class ScholarshipBase():

    def __init__(self, university_id, translations):
        self.university_id = university_id
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.translations[language].scholarship_string = translations[language]["scholarship_string"]

    @classmethod
    def create(cls, university_id, translations):
        university_id = int(university_id)
        scholarship_obj = cls(university_id, translations)
        db.session.add(scholarship_obj)
        db.session.commit()
        return scholarship_obj

    def json(self):
        return {
            "scholarship_id": getattr(self, "scholarship_id", -1),
            "university_name": self.university.university_name,
            "scholarship": self.current_translation.scholarship_string
        }

class Scholarship(ScholarshipBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Scholarship"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    scholarship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="scholarships")

class ScholarshipTranslation(translation_base(Scholarship)):
    __tablename__ = 'ScholarshipTranslation'
    scholarship_string = sa.Column(sa.Unicode(80))
    unique_scholarship_constraint = sa.PrimaryKeyConstraint('id', 'scholarship_string', 'locale', name='ufc_1')

class ScholarshipPending(pending_university_detail(Scholarship), ScholarshipBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "ScholarshipPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_scholarship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pending_uni_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship('UniversityPending', back_populates="scholarships")

class ScholarshipPendingTranslation(translation_base(ScholarshipPending), TranslationMixin):
    __tablename__ = 'ScholarshipPendingTranslation'
    scholarship_string = sa.Column(sa.Unicode(80))
    unique_scholarship_constraint = sa.PrimaryKeyConstraint('id', 'scholarship_string', 'locale', name='ufc_1')
