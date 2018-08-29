import logging
import json

from flask import g, request, redirect, jsonify, url_for, Response, abort
import flask_login

from app.models.university import University, UniversityPending
from app.models.course import Course
from app.models.tuition_fee import TuitionFeePending
from app.models.contact_detail import ContactDetailPending
from app.models.scholarship import ScholarshipPending
from app.models.facility import FacilityPending
from app.models.admission import AdmissionPending

from app import app

from app.views.request_utils import get_request_languages, get_req_list_by_language, get_req_data_by_language, get_i18n_list, zip_and_tag_request_data_lists

@app.route("/gallery/<university_id>/edit", methods=['POST'])
@flask_login.login_required
def edit_gallery(university_id):
    if request.method == 'POST':
        print(request.form)
        pending_university = UniversityPending.get_single_by_id(int(university_id))
        
        if pending_university is None:
            existing_university = University.get_single(university_id=university_id)
            if existing_university is None:
                logger.info("University id %d does not exist", university_id)                
                abort(400)
            pending_university = UniversityPending.edit(existing_university)

        return json.dumps(pending_university.json())