import json

import flask_login

import sqlalchemy
from sqlalchemy_i18n import Translatable, translation_base

from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class Course(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Course"
    lang = "en"

    course_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Category.category_id'))

    def __init__(self, course_name, category_id, lang):
        self.translations[lang].course_name = course_name
        self.category_id = category_id

    def __repr__(self):
        names = ', '.join([v.course_name or "None" for k, v in self.translations.items()])
        return "<ID: %d, Name(s): '%s', Category: '%s'>" % (self.course_id, names, self.category_id)

    def json(self, lang):
        return {
            "course_name": self.translations[lang].course_name,
            "category_name": self.category.category_name
        }

    def all_translations(self):
        return {k: v.course_name or "None" for k, v in self.translations.items()}

    def add_name(self, course_name, lang):
        self.translations[lang].course_name = course_name
        db.session.commit()

    @classmethod
    def create(cls, course_name, category_id, lang):
        course = cls(course_name, category_id, lang)
        db.session.add(course)
        db.session.commit()
        return course

    @classmethod
    def get_single_by_id(cls, course_id):
        try:
            return db.session.query(cls).filter(cls.course_id==course_id).one()
        except:
            return None

    @classmethod
    def get_single_by_name(cls, course_name, lang):
        for c in db.session.query(cls).options(sqlalchemy.orm.joinedload(cls.translations[lang])).all():
            if (c.translations[lang].course_name == course_name):
                return c

        return None

class CourseTranslation(translation_base(Course)):
    __tablename__ = 'course_translation'
    course_name = sqlalchemy.Column(sqlalchemy.Unicode(80))
