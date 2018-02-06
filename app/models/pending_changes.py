import logging
from collections import namedtuple

PendingChanges = namedtuple("PendingChanges", ["additions", "edits", "deletions"])

from app.database import db

logger = logging.getLogger(__name__)

def pending_university_detail(ParentClass, target_id_name):
    
    class PendingUniversityDetail:
        def __init__(self, pending_uni_id, translations):
            self.pending_uni_id = pending_uni_id
            self.set_translations(translations)

        def kwargs(self):
            """ To be overridden by subclass if extra constuctor args are required """
            return {}

        @classmethod
        def addition(cls, pending_id, translations, **kwargs):
            pending_object = cls(pending_id, translations, **kwargs)
            pending_object.pending_type = "add_edit"
            pending_object.save()
            logger.info("Creating pending addition of %s", pending_object)
            return pending_object

        @classmethod
        def deletion(cls, to_delete):
            pending_object = cls(to_delete.university.university_id, {}, **to_delete.kwargs())
            pending_object.pending_type = "del"
            setattr(pending_object, target_id_name, getattr(to_delete, target_id_name))
            pending_object.save()
            return pending_object

        def approve(self, university_id):
            if self.pending_type == "add_edit":
                if getattr(self, target_id_name):
                    logger.info("Approving pending add of %s", self)
                    ParentClass.get_single(target_id_name=getattr(self, target_id_name)).set_translations(self.translations)
                else:
                    logger.info("Approving pending edit of %s", self)
                    ParentClass.create(university_id, self.translations, **self.kwargs())

            self.delete()

    return PendingUniversityDetail