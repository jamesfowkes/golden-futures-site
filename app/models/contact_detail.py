import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase

class ContactDetail(Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "ContactDetail"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    contact_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="contact_details")

    def __init__(self, university_id, contact_detail, language):
        self.university_id = university_id
        self.translations[language].contact_detail_string = contact_detail

    @classmethod
    def create(cls, university_id, contact_detail, language=None):
        university_id = int(university_id)
        contact_detail_obj = cls(university_id, contact_detail, language)
        db.session.add(contact_detail_obj)
        db.session.commit()
        return contact_detail_obj

    def json(self):
        return {
            "contact_detail_id": self.contact_detail_id, 
            "university_name": self.university.university_name,
            "contact_detail": self.current_translation.contact_detail_string
        }

class ContactDetailTranslation(translation_base(ContactDetail)):
    __tablename__ = 'ContactDetailTranslation'
    contact_detail_string = sa.Column(sa.Unicode(80))
    unique_contact_detail_constraint = sa.PrimaryKeyConstraint('id', 'contact_detail_string', 'locale', name='ufc_1')
