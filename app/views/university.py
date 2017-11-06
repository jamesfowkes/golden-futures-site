import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.university import UniversityPending

from app import app

@app.route("/university/create", methods=['POST'])
@flask_login.login_required
def create_university():
    if request.method == 'POST':
        university = UniversityPending.create(
            request.form["university_name"],
            request.form["language"]
        )
        return json.dumps(university.json())

@app.route("/university/<university_id>/translate", methods=['POST'])
@flask_login.login_required
def add_university_translation(university_id):
    if request.method == 'POST':
        university = UniversityPending.get_single_by_id(int(university_id))
        university.add_translated_name(
            request.form["university_name"],
            request.form["language"]
        )
        return json.dumps(university.json())
        