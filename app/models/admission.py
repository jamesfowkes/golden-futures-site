import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base

import app
from app.database import db
from app.models.base_model import BaseModelTranslateable, DeclarativeBase, TranslationMixin, get_locales

class AdmissionBase():

    def __init__(self, university_id, translations):
        self.university_id = university_id
        self.set_translations(translations)

    def set_translations(self, translations):
        for language in get_locales(translations):
            if "admission_string" in translations[language]:
                self.translations[language].admission_string = translations[language]["admission_string"]

    @classmethod
    def create(cls, university_id, translations):
        university_id = int(university_id)
        admission_obj = cls(university_id, translations)
        db.session.add(admission_obj)
        db.session.commit()
        return admission_obj

    def json(self):
        return {
            "admission_id": self.admission_id, 
            "university_name": self.university.university_name,
            "admission": self.current_translation.admission_string
        }

class Admission(AdmissionBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "Admission"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    admission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'))
    university = db.relationship('University', back_populates="admissions")

class AdmissionTranslation(translation_base(Admission)):
    __tablename__ = 'AdmissionTranslation'
    admission_string = sa.Column(sa.Unicode(80))
    unique_admission_constraint = sa.PrimaryKeyConstraint('id', 'admission_string', 'locale', name='ufc_1')

class AdmissionPending(AdmissionBase, Translatable, BaseModelTranslateable, DeclarativeBase):

    __tablename__ = "AdmissionPending"
    __translatable__ = {'locales': app.app.config["SUPPORTED_LOCALES"]}
    locale = 'en'

    pending_admission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('Admission.admission_id'), nullable=True)
    pending_uni_id = db.Column(db.Integer, db.ForeignKey('UniversityPending.pending_id'))
    university = db.relationship('UniversityPending', back_populates="admissions")
    pending_type = db.Column(db.String(6), nullable=False)

    def __init__(self, pending_uni_id, translations):
        self.pending_uni_id = pending_uni_id
        self.set_translations(translations)

    def approve(self, university_id):
        if self.pending_type == "add_edit":
            if self.admission_id:
                Admission.get_single(admission_id=self.admission_id).set_translations(self.translations)
            else:
                Admission.create(university_id, self.translations)

        self.delete()

    @classmethod
    def addition(cls, pending_uni_id, translations):
        admission_obj = cls(pending_uni_id, translations)
        admission_obj.pending_type = "add_edit"
        db.session.add(admission_obj)
        db.session.commit()
        return admission_obj

class AdmissionPendingTranslation(translation_base(AdmissionPending), TranslationMixin):
    __tablename__ = 'AdmissionPendingTranslation'
    admission_string = sa.Column(sa.Unicode(80))
    unique_admission_constraint = sa.PrimaryKeyConstraint('id', 'admission_string', 'locale', name='ufc_1')