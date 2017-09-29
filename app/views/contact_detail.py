import json

from flask import request, redirect, url_for, Response, abort
import flask_login

from app.models.contact_detail import ContactDetail

from app import app

from app.locale import get_locale

@app.route("/contact_detail/create", methods=['POST'])
@flask_login.login_required
def create_contact_detail():
    if request.method == 'POST':
        contact_detail = ContactDetail.create(request.form["university_id"], request.form["contact_detail"], get_locale())
        return json.dumps(contact_detail.json())