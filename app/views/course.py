import logging
import json

from flask import request, redirect, url_for, Response, abort, g, jsonify
import flask_login

from app.models.course import Course, CoursePending

from app import app

logger = logging.getLogger(__name__)

@app.route("/course/create", methods=['POST'])
@flask_login.login_required
def create_course():
    if request.method == 'POST':
        course_name = request.form["course_name"]
        language = request.form["language"]
        logger.info("Creating new pending course %s", course_name)
        pending_course = CoursePending.addition(course_name, language)
        return jsonify({
            "success": True,
            "data": pending_course.json(),
            "redirect": url_for('dashboard.render_courses_dashboard')
        })


@app.route("/course/edit/<course_id>", methods=['POST'])
@flask_login.login_required
def edit_course(course_id):
    if request.method == 'POST':
        course_name = request.form["course_name"]
        language = request.form["language"]

        course_to_edit = Course.get_single_by_id(course_id)
        pending_course = CoursePending.edit(course_to_edit)
        pending_course.translations[language].course_name = course_name
        return jsonify({
            "success": True,
            "data": pending_course.json(),
            "redirect": url_for('dashboard.render_courses_dashboard')
        })

@app.route("/course/editpending/<pending_id>", methods=['POST'])
@flask_login.login_required
def edit_pending_course(pending_id):
    if request.method == 'POST':
        course_name = request.form["course_name"]
        language = request.form["language"]

        course_pending = CoursePending.get(pending_id=pending_id).one()
        logger.info("New name for '%s': '%s'", course_pending.course_name, course_name)
        course_pending.set_name(course_name, language)
        return jsonify({
            "success": True,
            "data": course_pending.json(),
            "redirect": url_for('dashboard.render_courses_dashboard')
        })

@app.route("/course/pending/approve", methods=['POST'])
@flask_login.login_required
def approve_pending_course_change():
    if request.method == 'POST':
        course_pending = CoursePending.get_single(pending_id=request.form["data_id"])
        json = course_pending.json()

        remaining_count = CoursePending.get_count(course_pending.pending_type) - 1

        logger.info("Approve pending change '%s' to course %s (%d remaining)", course_pending.pending_type, course_pending.course_name, remaining_count)

        course_pending.approve()

        return jsonify({
            "success" : True,
            "data": json,
            "remaining_count": remaining_count
        })

@app.route("/course/pending/reject", methods=['POST'])
@flask_login.login_required
def reject_pending_course_change():
    if request.method == 'POST':
        course_pending = CoursePending.get_single(pending_id=request.form["data_id"])
        json = course_pending.json()

        remaining_count = CoursePending.get_count(course_pending.pending_type) - 1
                
        logger.info("Rejecting pending change '%s' to course %s", course_pending.pending_type, course_pending.course_name)
        
        course_pending.reject()
        
        return jsonify({
            "success" : True,
            "data": json,
            "remaining_count": remaining_count
        })
