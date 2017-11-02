import logging
import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.category import Category

from app import app

logger = logging.getLogger(__name__)

@app.route("/category/create", methods=['POST'])
@flask_login.login_required
def create_category():
    if request.method == 'POST':
        category_name = request.form["category_name"]
        language = request.form["langauge"]
    else:
        category_name = request.args["category_name"]
        language = request.args["langauge"]

    logger.info("Creating category {} in langauge {}".format(category_name, language))
    category = Category.create(category, language)
    return json.dumps(category.json())

@app.route("/<language>/category/delete", methods=['POST'])
@flask_login.login_required
def delete_category(language):
    if request.method == 'POST':
        category = Category.get_single(category_name=request.form["category_name"], language=language)
        if len(category.courses):
            abort(409)

        category.delete()

        return Response(200)
        
