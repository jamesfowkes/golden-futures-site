import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.quote import Quote, QuotePending

from app import app

from app.locale import get_locale

@app.route("/quote/create", methods=['POST'])
@flask_login.login_required
def create_quote():
    if request.method == 'POST':
        quote = QuotePending.addition(
            request.form["university_id"],
            {request.form["language"]: {"quote_string": request.form["quote"]}}
        )

        return json.dumps(quote.json())
