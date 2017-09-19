import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.facility import Facility

from app.application import app

from app.locale import get_locale

@app.route("/facility/create", methods=['POST'])
@flask_login.login_required
def create_facility():
    if request.method == 'POST':
        facility = Facility.create(request.form["university_id"], request.form["facility"], get_locale())
        return json.dumps(facility.json())
