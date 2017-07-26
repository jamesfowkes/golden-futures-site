from flask import request, redirect, url_for, Response
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
            return user.json()
        else:
            return Response(status=403)

@app.route("/user/login", methods=['POST'])
def login_user():
    if request.method == 'POST':
        pending_login_user = User.get_single(username=request.form["username"])
        if pending_login_user and pending_login_user.match_password(request.form["password"]):
            pending_login_user.login()
            return redirect(url_for("render_index"))

    return Response(status=403)