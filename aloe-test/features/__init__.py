import os

import aloe

os.environ["GF_CONFIG_CLASS"] = "config.AloeConfig"

from app.application import app
from app.database import db
from app.models.user import User

@aloe.before.each_example
def before_each_scenario(scenario, outline, steps):
    db.create_all()
    aloe.world.app = app.test_client()

    for user in User.get():
        user.delete()

    User.create('standard', 'Standard Smith', 'standard', False)
    User.create('admin', 'Admin Smith', 'admin', True)
