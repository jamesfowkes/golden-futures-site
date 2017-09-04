import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

from app.database import db

from app.models.base_model import BaseModelTranslateable, DeclarativeBase

from app.models.university_course_map import university_course_map_table

class University(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "University"
    locale = "en"

    university_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courses = db.relationship('Course', secondary=university_course_map_table, back_populates="universities")

    def __init__(self, university_name, language):
        self.translations[language].university_name = university_name

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.university_id, self.university_name)

    def json(self):
        return {"university_id": self.university_id, "university_name": self.current_translation.university_name, "language": self.locale}
            
    @classmethod
    def create(cls, university_name, language=None):
        language = language or g.current_lang
        university = cls(university_name, language)
        db.session.add(university)
        db.session.commit()
        return university

    @classmethod
    def get_by_name(cls, university_name):
        return cls.get(university_name=university_name).all()

class UniversityTranslation(translation_base(University)):
    __tablename__ = 'university_translation'
    university_name = sa.Column(sa.Unicode(80))