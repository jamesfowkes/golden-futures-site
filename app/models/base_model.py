import sqlalchemy

from app.database import db

class BaseModel:

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def get_single(cls, **kwargs):
        try:
            return cls.query.filter_by(**kwargs).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None