import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.scholarship import Scholarship

from app import app

from app.locale import get_locale

@app.route("/scholarship/create", methods=['POST'])
@flask_login.login_required
def create_scholarship():
    if request.method == 'POST':
        scholarship = Scholarship.create(request.form["university_id"], request.form["scholarship"], get_locale())
        return json.dumps(scholarship.json())
