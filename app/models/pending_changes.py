from collections import namedtuple

from app.database import db

from app.models.university import UniversityPending
from app.models.category import CategoryPending
from app.models.course import CoursePending
from app.models.admission import AdmissionPending
from app.models.scholarship import ScholarshipPending
from app.models.tuition_fee import TuitionFeePending
from app.models.contact_detail import ContactDetailPending
from app.models.facility import FacilityPending

class PendingChanges():
    def __init__(self, adds, edits, dels):
        self.additions = adds
        self.edits = edits
        self.deletions = dels

    @classmethod
    def all(cls):
        additions = {
            "category": CategoryPending.additions()
        }

        edits = {
            "category": CategoryPending.edits()
        }

        deletions = {
            "category": CategoryPending.deletions()
        }
        
        return cls(additions, edits, deletions)
