import logging
import json

from flask import request, redirect, jsonify, url_for, Response, abort
import flask_login

from app.models.category import CategoryPending

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
    category = CategoryPending.addition(category_name, language)
    category.set_intro(category_intro)
    category.set_careers(category_careers)
    return json.dumps(category.json())

@app.route("/<language>/category/delete", methods=['POST'])
@flask_login.login_required
def delete_category(language):
    if request.method == 'POST':
        category = CategoryPending.get_single(category_name=request.form["category_name"], language=language)
        if len(category.courses):
            abort(409)

        category.delete()

        return Response(200)
        
@app.route("/category/pending/approve", methods=['POST'])
@flask_login.login_required
def approve_pending_change():
    if request.method == 'POST':
        category_pending = CategoryPending.get_single(pending_id=request.form["category_id"])
        logger.info("Approve pending change '%s' to category %s", category_pending.pending_type, category_pending.category_name)
        category_pending.approve()
        return jsonify(result=True)

@app.route("/category/pending/reject", methods=['POST'])
@flask_login.login_required
def reject_pending_change():
    if request.method == 'POST':
        category_pending = CategoryPending.get_single(pending_id=request.form["category_id"])
        logger.info("Rejecting pending change '%s' to category %s", category_pending.pending_type, category_pending.category_name)
        category_pending.reject()
        return jsonify(result=True)
