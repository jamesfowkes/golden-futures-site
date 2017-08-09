import json

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

from app.database import db

from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class Category(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Category"
    locale = "en"

    category_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    courses = sa.orm.relationship('Course', backref="category")

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.category_id, self.category_name)

    def json(self, lang):
        return {"category_name": self.category_name, "courses": [c.course_name for c in self.courses]}

    @classmethod
    def create(cls, category_name):
        category = cls(category_name)
        db.session.add(category)
        db.session.commit()
        return category

class CategoryTranslation(translation_base(Category)):
    __tablename__ = 'category_translation'
    category_name = sa.Column(sa.Unicode(80))
