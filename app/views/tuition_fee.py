import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.tuition_fee import TuitionFeePending

from app import app

@app.route("/tuition_fee/create", methods=['POST'])
@flask_login.login_required
def create_tuition_fee():
    if request.method == 'POST':
        tuition_fee = TuitionFeePending.create(
            request.form["university_id"],
            request.form["tuition_fee"],
            request.form["tuition_fee"],
            request.form["currency"],
            request.form["period"],
            request.form["award"],
            request.form["language"]
        )
        return json.dumps(tuition_fee.json())
