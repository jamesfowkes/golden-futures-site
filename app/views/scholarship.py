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
        university = request.form["university_id"]
        scholarship = request.form["scholarship"]
        language = request.form["language"]
        logger.info("Creating scholarship %s (%s)", university, scholarship)
        scholarship = ScholarshipPending.create(
            university, scholarship, language
        )
        return json.dumps(scholarship.json())
