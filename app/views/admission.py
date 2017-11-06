import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.admission import Admission, AdmissionPending

from app import app

from app.locale import get_locale

@app.route("/admission/create", methods=['POST'])
@flask_login.login_required
def create_admission():
    if request.method == 'POST':
        admission = AdmissionPending.create(
        	request.form["university_id"], request.form["admission"], request.form["language"])
        return json.dumps(admission.json())
