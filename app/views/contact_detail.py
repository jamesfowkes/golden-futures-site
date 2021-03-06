import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.contact_detail import ContactDetailPending

from app import app

from app.locale import get_locale

@app.route("/contact_detail/create", methods=['POST'])
@flask_login.login_required
def create_contact_detail():
    if request.method == 'POST':
        contact_detail = ContactDetailPending.addition(
        	request.form["university_id"],
        	{request.form["language"]: {"contact_detail_string": request.form["contact_detail"]}}
        )
        return json.dumps(contact_detail.json())
