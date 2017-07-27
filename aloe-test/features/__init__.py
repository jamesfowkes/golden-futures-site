import os

import aloe

os.environ["GF_CONFIG_CLASS"] = "config.AloeConfig"

from app.application import app
from app.database import db
from app.models.user import User
from app.models.course import Course
from app.models.category import Category

@aloe.before.each_example
def before_each_scenario(scenario, outline, steps):
    db.create_all()
    aloe.world.app = app.test_client()

    for user in User.get():
        user.delete()

    for course in Course.get():
        course.delete()

    for category in Category.get():
        category.delete()

    User.create('standard', 'Standard Smith', 'standard', False)
    User.create('admin', 'Admin Smith', 'admin', True)
