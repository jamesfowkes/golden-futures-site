import json

from flask import request, redirect, url_for, Response, abort, g
import flask_login

from app.models.course import Course

from app import app

@app.route("/course/create", methods=['POST'])
@flask_login.login_required
def create_course():
    if request.method == 'POST':
        course_name = request.form["course_name"]
        category_id = request.form["category_id"]
        language = request.form["language"]
        course = Course.create(course_name, language, category_id)
        return json.dumps(course.json())

@app.route("/course/<course_id>/translate", methods=['POST'])
@flask_login.login_required
def add_course_translation(lang, course_id):
    if request.method == 'POST':
        course = Course.get_single_by_id(course_id)
        course.add_name(request.form["course_name"], lang)
        return json.dumps(course.json(lang))
