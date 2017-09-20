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

@aloe.before.each_example
def before_each_scenario(scenario, outline, steps):

    aloe.world.language = "en"

    with app.app_context():
        aloe.world.app = current_app.test_client()

        DeclarativeBase.metadata.drop_all(bind=db.engine)
        DeclarativeBase.metadata.create_all(bind=db.engine)

        for user in User.get():
            user.delete()

        for course in Course.get():
            course.delete()

        for category in Category.get():
            category.delete()

        User.create('standard', 'Standard Smith', 'standard', False)
        User.create('admin', 'Admin Smith', 'admin', True)

