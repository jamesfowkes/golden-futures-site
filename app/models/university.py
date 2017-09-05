import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase
from app.models.university_course_map import university_course_map_table

class University(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "University"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    university_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courses = db.relationship('Course', secondary=university_course_map_table, back_populates="universities")

    def __init__(self, university_name, language):
        self.translations[language].university_name = university_name

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.university_id, self.university_name)

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

class UniversityTranslation(translation_base(University)):
    __tablename__ = 'university_translation'
    university_name = sa.Column(sa.Unicode(80))