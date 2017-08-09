import json

import flask_login

from app.database import db

from app.models.base_model import BaseModel, DeclarativeBase

class Category(BaseModel, DeclarativeBase):

    __tablename__ = "Category"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(80))
    courses = db.relationship('Course', backref="category")
    language = db.Column(db.String(10))

    __table_args__ = (db.UniqueConstraint('category_name', 'language', name='_category_unique_cons'),)

    def __init__(self, category_name, language):
        self.category_name = category_name
        self.language = language

    def __repr__(self):
        return "<ID: '%d', Name: '%s'>" % (self.category_id, self.category_name)

    def json(self):
        return {"category_name": self.category_name, "language": self.language}

    @classmethod    
    def get_single(cls, category_name, language=None):
        result = db.session.query(cls).filter_by(category_name=category_name)
        if language:
            result = result.filter_by(language=language)

        try:
            return result.one()
        except:
            return None
            
    @classmethod
    def create(cls, category_name, language):
        category = cls(category_name, language)
        db.session.add(category)
        db.session.commit()
        return category
