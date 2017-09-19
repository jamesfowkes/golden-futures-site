import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.tuition_fee import TuitionFee

from app.application import app

from app.locale import get_locale

@app.route("/tuition_fee/create", methods=['POST'])
@flask_login.login_required
def create_tuition_fee():
    if request.method == 'POST':
        tuition_fee = TuitionFee.create(request.form["university_id"], request.form["tuition_fee"], request.form["currency"], request.form["period"], request.form["award"], get_locale())
        return json.dumps(tuition_fee.json())
