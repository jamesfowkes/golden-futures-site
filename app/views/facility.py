import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.facility import FacilityPending

from app import app

from app.locale import get_locale

@app.route("/facility/create", methods=['POST'])
@flask_login.login_required
def create_facility():
    if request.method == 'POST':
        facility = FacilityPending.create(
        	request.form["university_id"], request.form["facility"], request.form["language"])
        return json.dumps(facility.json())
