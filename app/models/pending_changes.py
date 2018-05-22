import logging
from collections import namedtuple

PendingChanges = namedtuple("PendingChanges", ["additions", "edits", "deletions"])

from app.database import db

logger = logging.getLogger(__name__)

def pending_university_detail(ParentClass):
    
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
            pending_object.save()
            logger.info("Creating pending addition of %s", pending_object)
            return pending_object

        def approve(self, university_id):
            logger.info("Approving add of %s", self)
            ParentClass.create(university_id, self.translations, **self.kwargs())

            self.delete()

        def reject(self):
            logger.info("Rejecting add of %s", self)
            self.delete()

    return PendingUniversityDetail
