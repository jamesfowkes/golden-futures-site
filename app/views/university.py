import logging
import json

from flask import request, redirect, jsonify, url_for, Response, abort
import flask_login

from app.models.university import University, UniversityPending
from app.models.course import Course
from app.models.tuition_fee import TuitionFeePending

from app import app

from app.views.request_utils import get_request_languages, get_req_list_by_language, get_req_data_by_language, get_i18n_list, zip_and_tag_request_data_lists

from pprint import pprint

logger = logging.getLogger(__name__)

def get_tuition_fee_request_data(request):
    data = zip_and_tag_request_data_lists(
        request, 
        ["university_tuition_fee_min[]", "university_tuition_fee_max[]"]
    )

    include_in_filter_indexes = [int(i) for i in request.form.getlist("university_tuition_fee_include_in_filter[]")]

    print(include_in_filter_indexes)
    for index, d in enumerate(data):
        d["translations"] = get_req_list_by_language(
            request, ["university_tuition_fee_award", "university_tuition_fee_period"], ["award", "period"]
        )

        d["include_in_filter[]"] = index in include_in_filter_indexes

    return data

@app.route("/university/create", methods=['POST'])
@flask_login.login_required
def create_university():
    if request.method == 'POST':

        languages = get_request_languages(request)
        data = get_req_data_by_language(request,
            ["university_name", "university_intro"]
        )

        university = UniversityPending.addition(data)

        return json.dumps(university.json())

@app.route("/university/<university_id>/edit", methods=['POST'])
@flask_login.login_required
def edit_university(university_id):
    if request.method == 'POST':
        pending_university = UniversityPending.get_single_by_id(int(university_id))
        
        if pending_university is None:
            existing_university = University.get_single(university_id=university_id)
            if existing_university is None:
                logger.info("University id %d does not exist", university_id)                
                abort(400)
            pending_university = UniversityPending.edit(existing_university)

        languages = get_request_languages(request)
        try:
            request_data = {
                "latlong": request.form["university_latlong"],
                "web_address": request.form["university_web_address"],
                "courses": request.form.getlist("courses[]"),
                "facilities": get_i18n_list(request, "university_facility"),
                "contact_details": get_i18n_list(request, "university_contact_detail"),
                "admissions": get_i18n_list(request, "university_admission"),
                "scholarships": get_i18n_list(request, "university_scholarship"),
                "translations": get_req_data_by_language(request, ["university_name", "university_intro"])
            }
        except KeyError as e:
            logging.error(e)
            raise

        pending_university.set_translations(request_data["translations"])

        pending_university.set_latlong(request_data["latlong"])
        pending_university.set_web_address(request_data["web_address"])

        tuition_fee_data = get_tuition_fee_request_data(request)
        print(tuition_fee_data)

        pending_university.remove_tuition_fees()
        for fee in tuition_fee_data:
            TuitionFeePending.addition(
                pending_university.pending_id,
                fee["translations"],
                tuition_fee_min=fee["university_tuition_fee_min[]"],
                tuition_fee_max=fee["university_tuition_fee_max[]"],
                include_in_filter=fee["include_in_filter[]"],
                currency="$"
            )

        pending_university.remove_courses()
        pending_university.add_courses([Course.get_single(course_id=int(c)) for c in request_data["courses"]])

        return json.dumps(pending_university.json())
        
@app.route("/university/pending/approve", methods=['POST'])
@flask_login.login_required
def approve_pending_university_change():
    if request.method == 'POST':
        university_pending = UniversityPending.get_single(pending_id=request.form["data_id"])
        json = university_pending.json()

        remaining_count = UniversityPending.get_similar_count(university_pending) - 1

        logger.info("Approve pending change '%s' to university %s", university_pending.pending_type, university_pending.university_name)
        university_pending.approve()

        return jsonify({
            "success" : True,
            "data": json,
            "remaining_count": remaining_count
        })

@app.route("/university/pending/reject", methods=['POST'])
@flask_login.login_required
def reject_pending_university_change():
    if request.method == 'POST':
        university_pending = UniversityPending.get_single(pending_id=request.form["data_id"])
        json = university_pending.json()

        remaining_count = UniversityPending.get_similar_count(university_pending) - 1

        logger.info("Rejecting pending change '%s' to university %s", university_pending.pending_type, university_pending.university_name)
        university_pending.reject()

        return jsonify({
            "success" : True,
            "data": json,
            "remaining_count": remaining_count
        })
