import logging
import json

from textwrap import shorten
from flask import request, redirect, jsonify, url_for, Response, abort
import flask_login
from flask_babel import gettext

from app.models.base_model import DbIntegrityException
from app.models.category import Category
from app.models.course import Course

from app.models.pending_models import CategoryPending, CoursePending

from app import app

logger = logging.getLogger(__name__)

@app.route("/category/create", methods=['POST'])
@flask_login.login_required
def create_category():
    if request.method == 'POST':
        category_name = request.form["category_name"]
        category_intro = request.form["category_intro"]
        category_careers = request.form["category_careers"]
        language = request.form["language"]
    else:
        category_name = request.args["category_name"]
        category_intro = request.args["category_intro"]
        category_careers = request.args["category_careers"]
        language = request.args["language"]

    logger.info("Creating category {} in language {}".format(category_name, language))
    try:
        category = CategoryPending.addition(category_name, language)
        category.set_intro(category_intro)
        category.set_careers(category_careers)

        data = {
            "success": True,
            "category_name": category.category_name,
            "entries": [
                gettext("New Category") +": " + category.category_name,
                gettext("Introduction") +": " + category.category_intro,
                gettext("Careers") +": " + category.category_careers
            ],
            "pending_id": category.pending_id
        }
    except DbIntegrityException:
        data = {
            "success": False,
            "err": gettext("This category already exists!")
        }
    except Exception as e:
        data = {
            "success": False,
            "err": gettext("An unknown error occured")
        }
        logger.error(e)
        raise
    return jsonify(data)

@app.route("/category/edit/<category_id>", methods=['POST'])
@flask_login.login_required
def edit_category(category_id):
    if request.method == 'POST':
        category_name = request.form["category_name"]
        category_intro = request.form["category_intro"]
        category_careers = request.form["category_careers"]
        courses = request.form.getlist("category_courses[]")
        language = request.form["language"]

        category = CategoryPending.get_single(category_id=category_id)
        
        if category is None:
            category = CategoryPending.edit(Category.get_single(category_id=category_id))

        logger.info("Saving pendings edits to category id %s", category_id)
        logger.info("New name: %s", category_name)
        logger.info("Intro: %s", shorten(category_intro, width=40, placeholder="..."))
        logger.info("Careers: %s", shorten(category_careers, width=40, placeholder="..."))
        logger.info("Courses: %s", ", ".join(courses))
        
        category.set_name(category_name, language)
        category.set_intro(category_intro, language)
        category.set_careers(category_careers, language)

        for course in category.courses:
            course.delete()
        for course in[Course.get_single(course_id=int(course_id)) for course_id in courses]:
            category.add_course(course)

        return jsonify({
            "success": True,
            "redirect": url_for("dashboard.render_edit_category_dashboard", category_id=category_id)
        })

    return jsonify({"success":False})

@app.route("/category/editpending/<pending_id>", methods=['POST'])
@flask_login.login_required
def edit_pending_category(pending_id):
    if request.method == 'POST':
        category_name = request.form["category_name"]
        category_intro = request.form["category_intro"]
        category_careers = request.form["category_careers"]
        courses = request.form.getlist("category_courses[]")
        language = request.form["language"]

        category = CategoryPending.get_single(pending_id=pending_id)

        logger.info("Saving pendings edits to category id %s", pending_id)
        logger.info("New name: %s", category_name)
        logger.info("Intro: %s", shorten(category_intro, width=40, placeholder="..."))
        logger.info("Careers: %s", shorten(category_careers, width=40, placeholder="..."))
        logger.info("Courses: %s", ", ".join(courses))
        
        category.set_name(category_name, language)
        category.set_intro(category_intro, language)
        category.set_careers(category_careers, language)

        for course in category.courses:
            course.delete()
        for course in[Course.get_single(course_id=int(course_id)) for course_id in courses]:
            category.add_course(course)

        return jsonify({
            "success": True,
            "redirect": url_for("dashboard.render_edit_pending_category_dashboard", pending_id=pending_id)
        })

    return jsonify({"success":False})

@app.route("/category/delete", methods=['POST'])
@flask_login.login_required
def delete_category():
    if request.method == 'POST':
        category = CategoryPending.get_single(category_name=request.form["category_name"], language=request.form["language"])
        if len(category.courses):
            abort(409)

        category.delete()

        return Response(200)


@app.route("/category/pending/approve", methods=['POST'])
@flask_login.login_required
def approve_pending_category_change():
    if request.method == 'POST':
        category_pending = CategoryPending.get_single(pending_id=request.form["data_id"])
        logger.info("Approve pending change '%s' to category %s", category_pending.pending_type, category_pending.category_name)
        category_pending.approve()
        return jsonify(result=True)

@app.route("/category/pending/reject", methods=['POST'])
@flask_login.login_required
def reject_pending_category_change():
    if request.method == 'POST':
        category_pending = CategoryPending.get_single(pending_id=request.form["data_id"])
        logger.info("Rejecting pending change '%s' to category %s", category_pending.pending_type, category_pending.category_name)
        category_pending.reject()
        return jsonify(result=True)
