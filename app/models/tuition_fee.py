import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class TuitionFeeBase():

    def __init__(self, university_id, tuition_fee_min, tuition_fee_max, currency, period, award, language):
        self.university_id = university_id
        self.translations[language].tuition_fee_min = tuition_fee_min
        self.translations[language].tuition_fee_max = tuition_fee_max
        self.translations[language].currency = currency
        self.translations[language].award = award
        self.translations[language].period = period

    def add_translation(self, translation, attr, language=None):
        if attr not in ["tuition_fee_min", "tuition_fee_max", "currency", "award", "period"]:
            raise Exception("Translatable attribute %s not recognised".format(attr))

        if language:
            setattr(self.translations[language], attr, translation)
        else:
            setattr(self.current_translation, attr, translation)

    @classmethod
    def create(cls, university_id, tuition_fee_min, tuition_fee_max, currency, period, award, language=None):
        university_id = int(university_id)
        tuition_fee_obj = cls(university_id, tuition_fee_min, tuition_fee_max, currency, period, award, language)
        db.session.add(tuition_fee_obj)
        db.session.commit()
        return tuition_fee_obj

    def json(self):
        return {
            "tuition_fee_id": self.tuition_fee_id, 
            "university_name": self.university.university_name,
            "tuition_fee_min": self.current_translation.tuition_fee_min,
            "tuition_fee_max": self.current_translation.tuition_fee_max,
            "currency": self.current_translation.currency,
            "award": self.current_translation.award,
            "period": self.current_translation.period
        }
    
    def __str__(self):

        if len(self.current_translation.period):
            period_string = " / {}".format(self.current_translation.period)
        else:
            period_string = ""

        if self.current_translation.tuition_fee_min == self.current_translation.tuition_fee_max:
            return "{award}: {currency}{tuition_fee_min} {period}".format(
                award = self.current_translation.award,
                currency = self.current_translation.currency,
                tuition_fee_min = self.current_translation.tuition_fee_min,
                period = period_string)
        else:
            return "{award}: {currency}{tuition_fee_min} - {currency}{tuition_fee_max} {period}".format(
                award = self.current_translation.award,
                currency = self.current_translation.currency,
                tuition_fee_min = self.current_translation.tuition_fee_min,
                tuition_fee_max = self.current_translation.tuition_fee_max,
                period = period_string)

class TuitionFee(TuitionFeeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "TuitionFee"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="tuition_fees")

class TuitionFeeTranslation(translation_base(TuitionFee)):
    __tablename__ = 'TuitionFeeTranslation'
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))

class TuitionFeePending(TuitionFeeBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "TuitionFeePending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pending_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship("UniversityPending", back_populates="tuition_fees")

    def __init__(self, pending_id, fee_min, fee_max, currency, award, period, language):
        self.pending_id = pending_id
        self.translations[language].tuition_fee_min = fee_min
        self.translations[language].tuition_fee_max = fee_max
        self.translations[language].currency = currency
        self.translations[language].award = award
        self.translations[language].period = period

    @classmethod
    def addition(cls, pending_id, fee_min, fee_max, currency, award, period, language):
        tuition_fee_obj = cls(pending_id, fee_min, fee_max, currency, award, period, language)
        db.session.add(tuition_fee_obj)
        db.session.commit()
        return tuition_fee_obj


class TuitionFeePendingTranslation(translation_base(TuitionFeePending)):
    __tablename__ = 'TuitionFeePendingTranslation'
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))
