import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.university import University

from app.application import app

from app.locale import get_locale

@app.route("/university/create", methods=['POST'])
@flask_login.login_required
def create_university():
    if request.method == 'POST':
        university = University.create(request.form["university_name"], get_locale())
        return json.dumps(university.json())

@app.route("/university/<university_id>/translate", methods=['POST'])
@flask_login.login_required
def add_university_translation(university_id):
    if request.method == 'POST':
        university = University.get_single_by_id(int(university_id))
        university.add_translated_name(request.form["university_name"])
        return json.dumps(university.json())
        