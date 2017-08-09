import json

import flask_login

from app.database import db
from app.models.base_model import BaseModel, DeclarativeBase

class Course(BaseModel, DeclarativeBase):

    __tablename__ = "Course"

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'))
    language = db.Column(db.String(10))
    course_name =  db.Column(db.String(80))

    __table_args__ = (db.UniqueConstraint('course_id', 'category_id', 'language', 'course_name', name='_course_unique_cons'),)

    def __init__(self, course_name, category_id, language):
        self.course_name = course_name
        self.language = language
        self.category_id = category_id

    def __repr__(self):
        return "<ID: %d, Lang: %s, Name(s): '%s', Category: '%s'>" % (self.course_id, self.language, self.course_name, self.category_id)

    def json(self):
        return {
            "course_name": self.course_name,
            "category_name": self.category.category_name
        }

    @classmethod
    def create(cls, course_name, category_id, language):
        course = cls(course_name, category_id, language)
        db.session.add(course)
        db.session.commit()
        return course

    @classmethod
    def get_by_name(cls, course_name):
        return db.session.query(cls).filter_by(course_name=course_name).all()

    @classmethod
    def get_single_by_id(cls, course_id):
        try:
            return db.session.query(cls).filter_by(course_id=course_id).one()
        except:
            return None

    @classmethod
    def get_single(cls, category, course_name, language):
        return db.session.query(cls).filter_by(course_name=course_name, category=category, language=language).one()
