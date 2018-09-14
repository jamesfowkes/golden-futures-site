import os

from flask import request, jsonify
from flask_dropzone import Dropzone
import flask_login

from app import app

basedir = os.path.abspath(os.path.dirname(__file__))

dropzone = Dropzone()

@flask_login.login_required
def image_upload(university_id):
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(os.path.join(basedir, app.config['IMAGES_PATH'][0], "pending"), f.filename))
       	return jsonify({"success" : True})

@flask_login.login_required
def image_remove(university_id):
    if request.method == 'GET':
        f = request.args["filename"]
        os.unlink(os.path.join(os.path.join(basedir, app.config['IMAGES_PATH'][0], "pending"), f))
       	return jsonify({"success" : True})

def init_app(app):
    dropzone.init_app(app)
    app.view_functions['image_upload'] = image_upload
    app.add_url_rule('/image_upload/pending/<university_id>', 'image_upload', image_upload, methods = ['POST'])
    app.add_url_rule('/image_remove/pending/<university_id>', 'image_remove', image_remove, methods = ['GET'])
