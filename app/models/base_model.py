import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from app.database import db

DeclarativeBase = declarative_base()  

class BaseModel():
        
    @classmethod
    def get(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs)

    @classmethod
    def get_single(cls, **kwargs):
        try:
            return db.session.query(cls).filter_by(**kwargs).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()