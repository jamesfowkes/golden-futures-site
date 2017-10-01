import logging

from flask import Blueprint, g, render_template, request, redirect
import jinja2

from app import app
from app.locale import get_locale

from app.models.university import University
from app.models.category import Category

logger = logging.getLogger(__name__)

website = Blueprint('website', __name__, template_folder='templates', url_prefix='/<lang>')

@jinja2.contextfilter
@website.app_template_filter()
def language_name(context, lang):
    return app.config["SUPPORTED_LOCALES"][lang]

@website.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang', g.lang)

@website.url_value_preprocessor
def pull_lang(endpoint, values):
    requested_language = values.pop('lang')
    logger.info("Requested: %s", requested_language)
    if requested_language in app.config["SUPPORTED_LOCALES"]:
        g.lang = requested_language
    else:
        g.lang = get_locale()
        logger.info("%s not supported, using %s from get_locale", requested_language, g.lang)

@website.route("/", methods=['GET'])
def render_index():
    g.active="index"
    target_template = "index." + g.lang + ".tpl"
    return render_template(target_template)

@website.route("/universities", methods=['GET'])
def render_universities():
    g.active="universities"
    all_universities = University.all()
    return render_template('universities.index.tpl', universities=all_universities)

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
    g.ep_data = {}

def init_app(app):
    app.register_blueprint(website)
    