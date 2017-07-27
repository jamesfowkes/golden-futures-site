import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.course import Course

from app.application import app

@app.route("/course/create", methods=['POST'])
@flask_login.login_required
def create_course():
    if request.method == 'POST':
        course = Course.create(request.form["course_name"], request.form["category_name"])
        return json.dumps(course.json())
