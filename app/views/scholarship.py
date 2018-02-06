import logging
import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.scholarship import ScholarshipPending

from app import app

logger = logging.getLogger(__name__)

@app.route("/scholarship/create", methods=['POST'])
@flask_login.login_required
def create_scholarship():
    if request.method == 'POST':
        facility = ScholarshipPending.addition(
            request.form["university_id"],
            {request.form["language"]: {"scholarship_string": request.form["scholarship"]}}
        )
        return json.dumps(facility.json())
