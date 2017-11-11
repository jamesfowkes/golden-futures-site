import json

from flask import request, redirect, url_for, Response, abort, g
import flask_login

from app.models.course import Course, CoursePending

from app import app

@app.route("/course/create", methods=['POST'])
@flask_login.login_required
def create_course():
    if request.method == 'POST':
        course_name = request.form["course_name"]
        category_id = request.form["category_id"]
        language = request.form["language"]
        course = CoursePending.create(course_name, language, category_id)
        return json.dumps(course.json())

@app.route("/course/edit/<course_id>", methods=['POST'])
@flask_login.login_required
def edit_course(course_id):
    if request.method == 'POST':
        course_name = request.form["course_name"]
        language = request.form["language"]

        course_to_edit = Course.get_single_by_id(course_id)
        pending_course = CoursePending.edit(course_to_edit)
        pending_course.translations["lang"].course_name = course_name
        return json.dumps({
            "success": True,
            "redirect": url_for('dashboard.render_courses_dashboard')
        })
