import logging

from flask import Blueprint, g, render_template, request, redirect
import jinja2

from app import app
from app.locale import get_locale

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
    target_template = "index." + g.lang + ".tpl"
    return render_template(target_template)

@website.route("/universities", methods=['GET'])
def render_universities():
    return render_template('university.index.tpl')

@website.route("/courses", methods=['GET'])
def render_courses():
    return render_template('course.index.tpl')

def init_app(app):
    app.register_blueprint(website)
    