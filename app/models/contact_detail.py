import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales
from app.models.pending_changes import pending_university_detail

class ContactDetailBase():

    def __init__(self, university_id, translations):
        self.university_id = university_id
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            self.translations[language].contact_detail_string = translations[language]["contact_detail_string"]

    @classmethod
    def create(cls, university_id, translations):
        university_id = int(university_id)
        contact_detail_obj = cls(university_id, translations)
        contact_detail_obj.save()
        return contact_detail_obj

    def json(self):
        return {
            "contact_detail_id": self.contact_detail_id, 
            "university_name": self.university.university_name,
            "contact_detail": self.current_translation.contact_detail_string
        }


class ContactDetail(ContactDetailBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "ContactDetail"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    contact_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="contact_details")

class ContactDetailTranslation(translation_base(ContactDetail)):
    __tablename__ = 'ContactDetailTranslation'
    contact_detail_string = sa.Column(sa.Unicode(80))
    unique_contact_detail_constraint = sa.PrimaryKeyConstraint('id', 'contact_detail_string', 'locale', name='ufc_1')

class ContactDetailPending(pending_university_detail(ContactDetail, "contact_detail_id"), ContactDetailBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "ContactDetailPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_contact_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('ContactDetail.contact_detail_id'), nullable=True)
    pending_uni_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship('UniversityPending', back_populates="contact_details")
    pending_type = db.Column(db.String(6), nullable=False)

class ContactDetailPendingTranslation(translation_base(ContactDetailPending), TranslationMixin):
    __tablename__ = 'ContactDetailPendingTranslation'
    contact_detail_string = sa.Column(sa.Unicode(80))
    unique_contact_detail_constraint = sa.PrimaryKeyConstraint('id', 'contact_detail_string', 'locale', name='ufc_1')
