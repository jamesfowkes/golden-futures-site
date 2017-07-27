import json

import flask_login

from app.database import db
from app.models.base_model import BaseModel

class Category(db.Model, BaseModel):

    __tablename__ = "Category"

    category_name = db.Column(db.String(80), primary_key=True)
    courses = db.relationship('Course')

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return "<Category Name '%s'>" % self.category_name

    def json(self):
        return {"category_name": self.category_name, "courses": [c.course_name for c in self.courses]}

    @classmethod
    def create(cls, category_name):
        category = cls(category_name)
        db.session.add(category)
        db.session.commit()
        return category
