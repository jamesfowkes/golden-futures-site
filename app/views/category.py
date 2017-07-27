import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.category import Category

from app.application import app

@app.route("/category/create", methods=['POST'])
@flask_login.login_required
def create_category():
    if request.method == 'POST':
        category = Category.create(request.form["category_name"])
        return json.dumps(category.json())

@app.route("/category/delete", methods=['POST'])
@flask_login.login_required
def delete_category():
    if request.method == 'POST':
        category = Category.get_single(category_name=request.form["category_name"])
        if len(category.courses):
            abort(409)

        category.delete()

        return Response(200)
        
