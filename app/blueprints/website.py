import logging

from flask import Blueprint, g, render_template, request, redirect
import jinja2

from app import app
from app.locale import get_locale
from app import session

from app.models.university import University
from app.models.category import Category

logger = logging.getLogger(__name__)

website = Blueprint('website', __name__, template_folder='templates')

@jinja2.contextfilter
@website.app_template_filter()
def language_name(context, lang):
    return app.config["SUPPORTED_LOCALES"][lang]

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
    data = {
        "universities": all_universities,
        "categories": all_categories
    }
    return render_template('universities.index.tpl', data=data)

@website.route("/university/<university_id>", methods=['GET'])
def render_university(university_id):
    g.active="universities"
    g.ep_data["university_id"] = university_id
    university = University.get_single_by_id(university_id)
    return render_template('university.index.tpl', university=university)

@website.route("/courses", methods=['GET'])
def render_courses():
    g.active="categories"
    all_categories = Category.all()
    return render_template('course.index.tpl', categories=all_categories)

@website.before_request
def init_request():
    g.lang = get_locale()
    session.set("lang", g.lang)
    g.ep_data = {}

def init_app(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.register_blueprint(website)
    