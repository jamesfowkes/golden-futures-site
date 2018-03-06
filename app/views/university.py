import logging
import json

from flask import request, redirect, jsonify, url_for, Response, abort
import flask_login

from app.models.university import University, UniversityPending

from app import app

from app.views.request_utils import get_request_languages, get_req_data_by_language

logger = logging.getLogger(__name__)

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

@app.route("/university/<university_id>/translate", methods=['POST'])
@flask_login.login_required
def add_university_translation(university_id):
    if request.method == 'POST':
        pending_university = UniversityPending.get_single_by_id(int(university_id))
        
        if pending_university is None:
            university = University.get_single_by_id(int(university_id))
            pending_university = UniversityPending.edit(university)

        pending_university.set_translations(
            {request.form["language"]: {"university_name": request.form["university_name"]}}
        )

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
