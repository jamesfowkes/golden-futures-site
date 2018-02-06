import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.tuition_fee import TuitionFeePending

from app import app

@app.route("/tuition_fee/create", methods=['POST'])
@flask_login.login_required
def create_tuition_fee():
    if request.method == 'POST':
        tuition_fee = TuitionFeePending.addition(
            request.form["university_id"],
            {
                request.form["language"]:
                {
                    "tuition_fee_min": request.form["tuition_fee_min"],
                    "tuition_fee_max": request.form["tuition_fee_max"],
                    "currency": request.form["currency"],
                    "period": request.form["period"],
                    "award": request.form["award"]
                }
            },
            include_in_filter=request.form.get("include_in_filter", True)
        )
        return json.dumps(tuition_fee.json())
