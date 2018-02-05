from collections import namedtuple

PendingChanges = namedtuple("PendingChanges", ["additions", "edits", "deletions"])

from app.database import db

def pending_university_detail(ParentClass, target_id_name):
    
    class PendingUniversityDetail:

        def __init__(self, pending_uni_id, translations):
            self.pending_uni_id = pending_uni_id
            self.set_translations(translations)
            
        @classmethod
        def addition(cls, pending_id, translations):
            pending_object = cls(pending_id, translations)
            pending_object.pending_type = "add_edit"
            pending_object.save()
            return pending_object

        @classmethod
        def deletion(cls, to_delete):
            pending_object = cls(to_delete.university.university_id, {})
            pending_object.pending_type = "del"
            setattr(pending_object, target_id_name, getattr(to_delete, target_id_name))
            pending_object.save()
            return pending_object

        def approve(self, university_id):
            if self.pending_type == "add_edit":
                if getattr(self, target_id_name):
                    ParentClass.get_single(target_id_name=getattr(self, target_id_name)).set_translations(self.translations)
                else:
                    ParentClass.create(university_id, self.translations)

            self.delete()

    return PendingUniversityDetail