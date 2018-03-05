import logging

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_i18n.utils import get_current_locale, all_translated_columns

from app.database import db

from app.models.pending_changes import PendingChanges

DeclarativeBase = declarative_base()  

logger = logging.getLogger(__name__)

def get_locales(translations_obj_or_dict):
    try:
        locales = translations_obj_or_dict.manager.options['locales']
    except AttributeError:
        locales = translations_obj_or_dict.keys()
    return list(locales)

def get_translation(translations_obj_or_dict, language, field_name):
    try:
        return getattr(translations_obj_or_dict[language], field_name)
    except AttributeError:
        pass

    try:
        return translations_obj_or_dict[language][field_name]
    except KeyError:
        return None

    return translation

class DbIntegrityException(Exception):
    pass
    
class __Deleteable__:
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class BaseModel(__Deleteable__):

    @classmethod
    def all(cls):
        return db.session.query(cls).all()
        
    @classmethod
    def get(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs)

    @classmethod
    def get_single(cls, **kwargs):
        try:
            return db.session.query(cls).filter_by(**kwargs).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def kwargs(self):
            """ To be overridden by subclass if extra constuctor args are required """
            return {}

class TranslationMixin:

    def __getitem__(self, key):
        try:
            return self.__getattribute__(key)
        except TypeError:
            logger.error("unexpected key '%s' (%s)", key, type(key))
            raise
        
class BaseModelTranslateable(__Deleteable__):

    def current_language(self):
        return get_current_locale(self)

    def translateable_fields(self):
        return [c.name for c in all_translated_columns(self)]

    def all_translations(self, language = None):
        fields = self.translateable_fields()
        return {language: {c:self.translations[language].__getattribute__(c) for c in fields} for language, translations in self.translations.items()}

    def kwargs(self):
            """ To be overridden by subclass if extra constuctor args are required """
            return {}
            
    def set_translation(self, translations_obj_or_dict, language, field_name):
        translation = get_translation(translations_obj_or_dict, language, field_name)
        if translation:
            logger.info("Setting translation '%s' in '%s' to %s", field_name, language, translation)
            setattr(self.translations[language], field_name, translation)
        else:
            logger.info("%s translation for %s not present", language, field_name)
            
    @classmethod
    def all(cls):
        return db.session.query(cls).options(sqlalchemy.orm.joinedload(cls.current_translation)).all()
        
    @classmethod
    def get(cls, **kwargs):
        return db.session.query(cls).options(sqlalchemy.orm.joinedload(cls.current_translation)).filter_by(**kwargs)

    @classmethod
    def get_single_with_language(cls, language, **kwargs):
        """
        This should be as simple as
        
        return db.session.query(cls).options(
                sqlalchemy.orm.joinedload(cls.translations[language])
            ).filter_by(**kwargs).one()

        but this returns all rows (not sure why), so have to manually go through the returned results
        looking for kwargs matches
        """

        try:
            #logger.info("Class: {}, lang: {}, params: {}".format(cls.__name__, language, kwargs))
            all_results_for_language = db.session.query(cls).options(
                sqlalchemy.orm.joinedload(cls.translations[language])).all()

            #logger.info("Got {} results: ".format(len(all_results_for_language)))
            for res in all_results_for_language:
                #logger.info(res)
                match = True

                for k,v in kwargs.items():
                    try:
                        attr = getattr(res.translations[language], k)
                    except KeyError:
                        attr = getattr(res, k)

                    #logger.info(attr)
                    #logger.info("%s: %s, %s", k, v, getattr(res, k))
                    match = match and attr == v

                if match:
                    return res

            return None
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

    def save(self):
        db.session.add(self)
        db.session.commit()

class PendingChangeBase():

    @classmethod
    def additions(cls):
        return db.session.query(cls).filter(cls.pending_type=="add_edit").filter(cls.category_id == None).all()

    @classmethod
    def edits(cls):
        return db.session.query(cls).filter(cls.pending_type=="add_edit").filter(cls.category_id != None).all()

    @classmethod
    def deletions(cls):
        return db.session.query(cls).filter(cls.pending_type=="del").all()

    @classmethod
    def all_by_type(cls):
        all_changes = cls.all();
        additions = [c for c in all_changes if c.pending_type == "add_edit" and c.is_addition()]
        edits = [c for c in all_changes if c.pending_type == "add_edit" and not c.is_addition()]
        dels = [c for c in all_changes if c.pending_type == "del"]

        return PendingChanges(additions, edits, dels)

    @classmethod
    def get_similar_count(cls, similar_to_change):
        all_pending_changes = cls.all_by_type()

        if similar_to_change.pending_type == "add_edit":
            if similar_to_change.is_addition():
                return len(all_pending_changes.additions)
            else:
                return len(all_pending_changes.edits)
        elif similar_to_change.pending_type == "del":
            return len(all_pending_changes.deletions)
        elif similar_to_change.pending_type == "all":
            return len(all_pending_changes)
