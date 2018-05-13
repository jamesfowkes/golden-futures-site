import logging

from flask import Blueprint, g, render_template, request, redirect, url_for
import flask_login

import jinja2

from app import app
from app.locale import get_locale
from app import session

from app.models.university import University
from app.models.category import Category
from app.models.course import Course

from app.models.pending_changes import PendingChanges

from app.blueprints import common

logger = logging.getLogger(__name__)

website = Blueprint('website', __name__, template_folder='templates')

@website.route("/", methods=['GET'])
def render_index():
    g.active="index"
    target_template = "index.tpl"
    return render_template(target_template)

@website.route("/universities", methods=['GET'])
def render_universities():
    g.active="universities"
    all_universities = University.all()
    all_categories = Category.all()
    g.ep_data["uni_latlong_data"] = [
        {
            "name": uni.university_name,
            "latlong":uni.latlong,
            "view_url": url_for("website.render_university", university_id=uni.university_id),
        }
        for uni in all_universities
    ]
    g.ep_data["university_icon_path"] = url_for("static", filename="leaflet/university.svg")

    data = {
        "universities": all_universities,
        "categories": all_categories
    }
    return render_template('universities.index.tpl', data=data)

@website.route("/university/<university_id>", methods=['GET'])
def render_university(university_id):
    university = University.get_single_by_id(university_id)

    g.active="universities"
    g.ep_data["university_id"] = university_id
    g.ep_data["latlong"] = university.latlong
    g.ep_data["university_icon_path"] = url_for("static", filename="leaflet/university.svg")
    g.ep_data["osm_url"] = "http://www.openstreetmap.org/?mlat=" + university.lat + "&mlon=" + university.long + "&zoom=14"
    return render_template('university.index.tpl', university=university)

@website.route("/courses", methods=['GET'])
def render_courses():
    g.active="categories"
    all_categories = Category.all()
    return render_template('course.index.tpl', categories=all_categories)

@website.route("/login", methods=['GET'])
def render_login():
    g.active="login"
    return render_template('login.index.tpl')

@website.route("/logout", methods=['GET'])
def logout():
    g.active="logout"
    flask_login.logout_user()
    return redirect(url_for("website.render_index"))

def init_app(app):
    website.before_request(common.init_request)
    website.add_app_template_filter(common.language_name)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.register_blueprint(website)
    