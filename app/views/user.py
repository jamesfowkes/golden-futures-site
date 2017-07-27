import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.user import User

from app.application import app

@app.route("/user/create", methods=['POST'])
@flask_login.login_required
def create_user():
    if request.method == 'POST':
        if flask_login.current_user.is_admin():
            username = request.form["username"]
            given_name = request.form["given_name"]
            password = request.form["password"]
            is_admin = request.form.get("is_admin", False)
            user = User.create(username, given_name, password, is_admin)
            return json.dumps(user.json())
        else:
            abort(403)

@app.route("/user/delete", methods=['POST'])
@flask_login.login_required
def delete_user():
    if request.method == 'POST':
        if flask_login.current_user.is_admin():
            user = User.get_single(username=request.form["username"])
            if user:
                user.delete()
                return Response(200)
            else:
                return Response(404)
        else:
            abort(403)

@app.route("/user/login", methods=['POST'])
def login_user():
    if request.method == 'POST':
        pending_login_user = User.get_single(username=request.form["username"])
        if pending_login_user and pending_login_user.match_password(request.form["password"]):
            if pending_login_user.login():
                return redirect(url_for("render_dashboard"))

    abort(401)

@app.route("/user/logout")
def logout_user():
    flask_login.logout_user()
    return redirect(url_for("render_index"))
