import json

import flask_login

from app.database import db
from app.models.base_model import BaseModel

class Course(db.Model, BaseModel):

    __tablename__ = "Course"

    course_name = db.Column(db.String(80), primary_key=True)
    category_name = db.Column(db.String(80), db.ForeignKey('Category.category_name'))

    def __init__(self, course_name, category_name):
        self.course_name = course_name
        self.category_name = category_name

    def __repr__(self):
        return "<Course Name '%s', Category '%s'>" % (self.course_name, self.category_name)

    def json(self):
        return {
            "course_name": self.course_name,
            "category_name": self.category_name
        }

    @classmethod
    def create(cls, course_name, category_name):
        course = cls(course_name, category_name)
        db.session.add(course)
        db.session.commit()
        return course
