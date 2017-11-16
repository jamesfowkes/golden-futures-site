import os
import inspect

from config import DebugConfig

os.environ["GF_CONFIG_CLASS"] = "config.ScriptingConfig"

from app import app
from app.database import db

from app.models.admission import Admission, AdmissionTranslation
from app.models.category import Category, CategoryTranslation
from app.models.contact_detail import ContactDetail, ContactDetailTranslation
from app.models.course import Course, CourseTranslation
from app.models.facility import Facility, FacilityTranslation
from app.models.scholarship import Scholarship, ScholarshipTranslation
from app.models.tuition_fee import TuitionFee, TuitionFeeTranslation
from app.models.university import University, UniversityTranslation

CLASSES = {
    "admission": [Admission, AdmissionTranslation],
    "category": [Category, CategoryTranslation],
    "contact_detail": [ContactDetail, ContactDetailTranslation],
    "course": [Course, CourseTranslation],
    "facility": [Facility, FacilityTranslation],
    "scholarship": [Scholarship, ScholarshipTranslation],
    "tuition_fee": [TuitionFee, TuitionFeeTranslation],
    "university": [University, UniversityTranslation]
}

FILE_HEADER = """
import logging

import json

from flask import g

import flask_login

import sqlalchemy as sa
from sqlalchemy_i18n import Translatable, translation_base
from sqlalchemy_i18n.utils import get_current_locale

import app
from app.database import db

from app.models.base_model import BaseModelTranslateable, DeclarativeBase
"""

def print_modified_class(c):

    lines = inspect.getsourcelines(c)[0]
    print(lines[0], end='')
    print("    __bind_key__='pending'")
    for l in lines[1:]:
        print(l, end='')
    print("")

def print_base_imports(classes):
    for k, v in classes.items():
        print("from app.models.{} import {}Base".format(k, v[0].__name__))
    print("")

if __name__ == "__main__":

    print(FILE_HEADER)

    print_base_imports(CLASSES)

    for k, v in CLASSES.items():
        print_modified_class(v[0])
        print_modified_class(v[1])
