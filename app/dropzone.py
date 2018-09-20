import os
import logging

from flask import request, jsonify, url_for
from flask_dropzone import Dropzone
import flask_login

from app import app
from app.blueprints.dashboard import dashboard

from app.models.university import University, UniversityPending

logger = logging.getLogger(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

dropzone = Dropzone()

@flask_login.login_required
@dashboard.route("/image_upload/pending/<university_id>", methods = ['POST'])
def image_upload(university_id):
    if request.method == 'POST':
        f = request.files.get('file')
        university = University.get_single_by_id(university_id=university_id)
        university.pend_new_image(f)
       	return jsonify({"success" : True})

@flask_login.login_required
@dashboard.route("/image_pend/<university_id>")
def image_pend(university_id):
    existing_filename = request.args.get("filename")
    
    university = University.get_single_by_id(university_id=university_id)
    result = university.pend_existing_image(existing_filename)

    return jsonify(result)

@flask_login.login_required
@dashboard.route("/clear_pending/<university_id>")
def clear_pending(university_id):
    university = University.get_single_by_id(university_id=university_id)
    university.clear_pending_images()
    return jsonify({"success" : True})

@flask_login.login_required
@dashboard.route("/image_submit_complete/<university_id>")
def image_submit_complete(university_id):
    university = University.get_single_by_id(university_id=university_id)
    university.order_pending_images(request.args.getlist("files[]"))
    UniversityPending.edit(university)

    return jsonify({"success" : True, "redirect": url_for("dashboard.render_edit_uni_gallery",university_id=university_id)})

def init_app(app):
    dropzone.init_app(app)
    app.view_functions['image_upload'] = image_upload
