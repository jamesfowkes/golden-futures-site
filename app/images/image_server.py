import os
import logging

from flask import send_from_directory
from flask_images import Images

images_dir = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)

def serve_image(filename):
    logger.info(images_dir)
    return send_from_directory(images_dir, filename)

def init_app(app):
    app.view_functions['serve_image'] = serve_image
    app.add_url_rule("/images/<path:filename>", "serve_image")
    images = Images(app)
