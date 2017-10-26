import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class Scholarship(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Scholarship"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    scholarship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="scholarships")

    def __init__(self, university_id, scholarship, language):
        self.university_id = university_id
        self.translations[language].scholarship_string = scholarship

    def add_translation(self, translation, language=None):
        if language:
            self.translations[language].scholarship_string = translation
        else:
            self.current_translation.scholarship_string = translation

    @classmethod
    def create(cls, university_id, scholarship, language=None):
        university_id = int(university_id)
        scholarship_obj = cls(university_id, scholarship, language)
        db.session.add(scholarship_obj)
        db.session.commit()
        return scholarship_obj

    def json(self):
        return {
            "scholarship_id": self.scholarship_id, 
            "university_name": self.university.university_name,
            "scholarship": self.current_translation.scholarship_string
        }

class ScholarshipTranslation(translation_base(Scholarship)):
    __tablename__ = 'ScholarshipTranslation'
    scholarship_string = sa.Column(sa.Unicode(80))
    unique_scholarship_constraint = sa.PrimaryKeyConstraint('id', 'scholarship_string', 'locale', name='ufc_1')
