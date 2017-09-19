from flask import request, redirect, url_for, Response
import flask_login

from app import app

@app.route("/dashboard", methods=['GET'])
@flask_login.login_required
def render_dashboard():
    return Response(200)
