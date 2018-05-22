import os

from flask import request, jsonify
from flask_dropzone import Dropzone

from app import app

basedir = os.path.abspath(os.path.dirname(__file__))

dropzone = Dropzone()

def image_upload(university_id):
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(os.path.join(basedir, app.config['IMAGE_DIRECTORY']), f.filename))

       	return jsonify({})

def init_app(app):
    dropzone.init_app(app)
    app.view_functions['image_upload'] = image_upload
    app.add_url_rule('/image_upload/<university_id>', 'image_upload', image_upload, methods = ['POST'])
