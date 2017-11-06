import logging

from flask import current_app

import os

import aloe

os.environ["GF_CONFIG_CLASS"] = "config.AloeConfig"

from app import app
from app.database import db
from app.models.user import User
from app.models.course import Course
from app.models.category import Category

from app.models.base_model import DeclarativeBase

from app.locale import set_testing_language_selector

logger = logging.getLogger(__name__)

#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@aloe.before.each_example
def before_each_scenario(scenario, outline, steps):

    aloe.world.language = "en"

    set_testing_language_selector(lambda: aloe.world.language)

    with app.test_request_context():

        logger.info("Creating scenario data...")

        aloe.world.app = current_app.test_client()

        DeclarativeBase.metadata.drop_all(bind=db.engine)
        DeclarativeBase.metadata.create_all(bind=db.engine)

        for user in User.get():
            user.delete()

        for course in Course.get():
            course.delete()

        for category in Category.get():
            category.delete()

        User.create('standard', 'Standard Smith', 'standard', False, "en")
        User.create('ordinaire', 'Ordinaire Smith', 'standard', False, "fr")
        User.create('admin', 'Admin Smith', 'admin', True, "en")

        logger.info("...done")
        