import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.university import University

from app.application import app

@app.route("/<language>/university/create", methods=['POST'])
@flask_login.login_required
def create_university(language):
    if request.method == 'POST':
        university = University.create(request.form["university_name"], language)
        return json.dumps(university.json())
