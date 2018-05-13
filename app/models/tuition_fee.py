import json

from collections import namedtuple

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales
from app.models.pending_changes import pending_university_detail

class TuitionFeeBase():

    def __init__(self, university_id, translations, **kwargs):
        self.university_id = university_id
        self.tuition_fee_min = kwargs.get("tuition_fee_min", None)
        self.tuition_fee_max = kwargs.get("tuition_fee_max", None)
        self.currency = kwargs.get("currency", None)
        self.include_in_filter = kwargs.get("include_in_filter", True)
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.translations[language].award = translations[language]["award"]
            self.translations[language].period = translations[language]["period"]

    @classmethod
    def create(cls, university_id, translations, **kwargs):
        university_id = int(university_id)
        tuition_fee_obj = cls(university_id, translations, **kwargs)
        tuition_fee_obj.save()
        return tuition_fee_obj

    def json(self):
        return {
            "tuition_fee_id": getattr(self, "tuition_fee_id", -1),
            "university_name": self.university.university_name,
            "tuition_fee_min": self.tuition_fee_min,
            "tuition_fee_max": self.tuition_fee_max,
            "currency": self.currency,
            "award": self.current_translation.award,
            "period": self.current_translation.period
        }
    
    def __str__(self):

        if len(self.current_translation.period):
            period_string = "/ {}".format(self.current_translation.period)
        else:
            period_string = ""

        if self.tuition_fee_min == self.tuition_fee_max:
            s = "{award}: {currency}{tuition_fee_min} {period}".format(
                award = self.current_translation.award,
                currency = self.currency,
                tuition_fee_min = self.tuition_fee_min,
                period = period_string)
        else:
            s = "{award}: {currency}{tuition_fee_min} - {currency}{tuition_fee_max} {period}".format(
                award = self.current_translation.award,
                currency = self.currency,
                tuition_fee_min = self.tuition_fee_min,
                tuition_fee_max = self.tuition_fee_max,
                period = period_string)

        return s

    def kwargs(self):
        return {
            "tuition_fee_min": self.tuition_fee_min,
            "tuition_fee_max": self.tuition_fee_max,
            "currency": self.currency,
            "include_in_filter" : self.include_in_filter
        }

class TuitionFee(TuitionFeeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "TuitionFee"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="tuition_fees")
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))
    include_in_filter = sa.Column(sa.Boolean, default=True)

class TuitionFeeTranslation(translation_base(TuitionFee)):
    __tablename__ = 'TuitionFeeTranslation'
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))

TuitionFeePendingDetail = pending_university_detail(TuitionFee)
class TuitionFeePending(TuitionFeePendingDetail, TuitionFeeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "TuitionFeePending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    def __init__(self, pending_uni_id, translations, **kwargs):
        TuitionFeePendingDetail.__init__(self, pending_uni_id, translations)
        TuitionFeeBase.__init__(self, pending_uni_id, translations, **kwargs)

    def kwargs(self):
        return {
            "tuition_fee_min": self.tuition_fee_min,
            "tuition_fee_max": self.tuition_fee_max,
            "currency": self.currency,
            "include_in_filter" : self.include_in_filter
        }

    pending_tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pending_uni_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship("UniversityPending", back_populates="tuition_fees")
    include_in_filter = sa.Column(sa.Boolean, default=True)
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))

class TuitionFeePendingTranslation(translation_base(TuitionFeePending), TranslationMixin):
    __tablename__ = 'TuitionFeePendingTranslation'
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))
