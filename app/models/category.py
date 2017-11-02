from functools import total_ordering

import json

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModelTranslateable, DeclarativeBase

from app.models.category_course_map import category_course_map_table

@total_ordering
class Category(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Category"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courses = db.relationship('Course', secondary=category_course_map_table, back_populates="categories")

    def __init__(self, category_name, language):
        self.translations[language].category_name = category_name

    def __hash__(self):
        return self.category_id
        
    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.category_id, self.current_translation.category_name)

    def __eq__(self, other):
        return self.current_translation.category_name == other.current_translation.category_name

    def __ne__(self, other):
        return self.current_translation.category_name != other.current_translation.category_name

    def __lt__(self, other):
        return self.current_translation.category_name < other.current_translation.category_name

    def json(self):
        return {"category_name": self.current_translation.category_name, "language": get_current_locale(self)}

    def set_name(self, category_name, lang):
        self.translations[lang].category_name = category_name
        db.session.commit()

    def set_intro(self, intro, lang=None):
        if lang:
            self.translations[lang].category_intro = intro
        else:
            self.current_translation.category_intro = intro

        db.session.commit()

    def set_careers(self, careers, lang=None):
        if lang:
            self.translations[lang].category_careers = careers
        else:
            self.current_translation.category_careers = careers

        db.session.commit()

    def add_course(self, course):
        self.courses.append(course)
        db.session.add(self)
        db.session.commit()

    def course_names(self):
        names = [c.course_name for c in self.courses]
        return sorted(names)

    @classmethod
    def create(cls, category_name, language):
        category = cls(category_name, language)
        db.session.add(category)
        db.session.commit()
        return category

class CategoryTranslation(translation_base(Category)):
    __tablename__ = 'CategoryTranslation'
    category_name = sa.Column(sa.Unicode(80), unique=True)
    category_intro = sa.Column(sa.Unicode())
    category_careers = sa.Column(sa.Unicode())