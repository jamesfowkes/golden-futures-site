import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from app.database import db

DeclarativeBase = declarative_base()  

class __Deleteable__:
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class BaseModel(__Deleteable__):
        
    @classmethod
    def get(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs)

    @classmethod
    def get_single(cls, **kwargs):
        try:
            return db.session.query(cls).filter_by(**kwargs).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

class BaseModelTranslateable(__Deleteable__):
        
    @classmethod
    def get(cls, **kwargs):
        return db.session.query(cls).options(sqlalchemy.orm.joinedload(cls.current_translation)).filter_by(**kwargs)

    @classmethod
    def get_single_with_language(cls, language, **kwargs):
        try:
            return db.session.query(cls).options(sqlalchemy.orm.joinedload(cls.translations[language])).filter_by(**kwargs).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None            

    @classmethod
    def get_single(cls, **kwargs):

        language = kwargs.pop("language", None)
        
        if language:
            return cls.get_single_with_language(language, **kwargs)
        else:
            try:
                return db.session.query(cls).options(sqlalchemy.orm.joinedload(cls.current_translation)).filter_by(**kwargs).one()
            except sqlalchemy.orm.exc.NoResultFound:
                return None