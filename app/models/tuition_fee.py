import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class TuitionFee(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "TuitionFee"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    tuition_fee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="tuition_fees")

    def __init__(self, university_id, tuition_fee_min, tuition_fee_max, currency, period, award, language):
        self.university_id = university_id
        self.translations[language].tuition_fee_min = tuition_fee_min
        self.translations[language].tuition_fee_max = tuition_fee_max
        self.translations[language].currency = currency
        self.translations[language].award = award
        self.translations[language].period = period

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
        
class TuitionFeeTranslation(translation_base(TuitionFee)):
    __tablename__ = 'TuitionFeeTranslation'
    tuition_fee_min = sa.Column(sa.Integer)
    tuition_fee_max = sa.Column(sa.Integer)
    currency = sa.Column(sa.Unicode(6))
    award = sa.Column(sa.Unicode(80))
    period = sa.Column(sa.Unicode(20))
