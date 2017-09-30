import json

import flask_login

from app.database import db
from app.models.base_model import BaseModel, DeclarativeBase

from app.models.university_course_map import university_course_map_table
from app.models.category_course_map import category_course_map_table

class Course(BaseModel, DeclarativeBase):

    __tablename__ = "Course"

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name =  db.Column(db.String(80), unique=True)
    language = db.Column(db.String(10))
    
    universities = db.relationship('University', secondary=university_course_map_table, back_populates="courses")
    categories = db.relationship('Category', secondary=category_course_map_table, back_populates="courses")

    __table_args__ = (db.UniqueConstraint('course_id', 'language', 'course_name', name='_course_unique_cons'),)

    def __init__(self, course_name, language):
        self.course_name = course_name
        self.language = language

    def __repr__(self):
        return "<ID: %d, Lang: %s, Name(s): '%s', Categories: '%s'>" % (self.course_id, self.language, self.course_name, ", ". join([c.category_name for c in self.categories]))

    def json(self):
        return {
            "course_name": self.course_name,
            "category_name": ", ".join([c.category_name for c in self.categories])
        }

    @classmethod
    def create(cls, course_name, language):
        course = cls(course_name, language)
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
    def get_single(cls, course_name, language):
        return db.session.query(cls).filter_by(course_name=course_name, language=language).one()
