import logging
import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales
from app.models.pending_changes import pending_university_detail

logger = logging.getLogger(__name__)

class QuoteBase():

    def __init__(self, university_id, translations):
        self.university_id = university_id
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.translations[language].quote_string = translations[language]["quote_string"]

    @classmethod
    def create(cls, university_id, translations):
        university_id = int(university_id)
        quote_obj = cls(university_id, translations)
        db.session.add(quote_obj)
        db.session.commit()
        return quote_obj

    def json(self):
        return {
            "quote_id": getattr(self, "quote_id", -1),
            "university_name": self.university.university_name,
            "quote": self.current_translation.quote_string
        }

    def __str__(self):
        return "Quote:" + "'" + self.translations["en"].quote_string + "'"

class Quote(QuoteBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Quote"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    quote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="quotes")

class QuoteTranslation(translation_base(Quote)):
    __tablename__ = 'QuoteTranslation'
    quote_string = sa.Column(sa.Unicode(80))
    unique_quote_constraint = sa.PrimaryKeyConstraint('id', 'quote_string', 'locale', name='ufc_1')

class QuotePending(pending_university_detail(Quote), QuoteBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "QuotePending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_quote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pending_uni_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship('UniversityPending', back_populates="quotes")

class QuotePendingTranslation(translation_base(QuotePending), TranslationMixin):
    __tablename__ = 'QuotePendingTranslation'
    quote_string = sa.Column(sa.Unicode(80))
    unique_quote_constraint = sa.PrimaryKeyConstraint('id', 'quote_string', 'locale', name='ufc_1')
