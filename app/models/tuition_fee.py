import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales

class TuitionFeeBase():

    def __init__(self, university_id, translations):
        self.university_id = university_id
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.translations[language].tuition_fee_min = translations[language]["tuition_fee_min"]
            self.translations[language].tuition_fee_max = translations[language]["tuition_fee_max"]
            self.translations[language].currency = translations[language]["currency"]
            self.translations[language].award = translations[language]["award"]
            self.translations[language].period = translations[language]["period"]

    @classmethod
    def create(cls, university_id, translations):
        university_id = int(university_id)
        tuition_fee_obj = cls(university_id, translations)
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

    pending_tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tuition_fee_id = db.Column(db.Integer, db.ForeignKey('TuitionFee.tuition_fee_id'), nullable=True)
    pending_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship("UniversityPending", back_populates="tuition_fees")
    pending_type = db.Column(db.String(6), nullable=False)

    def __init__(self, pending_id, translations):
        self.pending_id = pending_id
        self.set_translations(translations)

    def approve(self, university_id):
        if self.pending_type == "add_edit":
            if self.tuition_fee_id:
                TuitionFee.get_single(tuition_fee_id=self.tuition_fee_id).update(self)
            else:
                TuitionFee.create(university_id, self.translations)

        self.delete()

    @classmethod
    def addition(cls, pending_id, translations):
        tuition_fee_obj = cls(pending_id, translations)
        tuition_fee_obj.pending_type = "add_edit"
        
        db.session.add(tuition_fee_obj)
        db.session.commit()
        return tuition_fee_obj


class TuitionFeePendingTranslation(translation_base(TuitionFeePending), TranslationMixin):
    __tablename__ = 'TuitionFeePendingTranslation'
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))
