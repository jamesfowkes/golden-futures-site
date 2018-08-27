import logging
from pathlib import Path 

import jinja2

from flask import g, url_for

from app import app, static_url_exists
from app import session
from app.locale import get_locale, get_js_strings

logger = logging.getLogger(__name__)

THIS_PATH = Path(__file__).parent

@jinja2.contextfilter
def language_name(context, lang):
    if "SUPPORTED_LOCALES" in app.config:
        try:
            return app.config["SUPPORTED_LOCALES"][lang]
        except KeyError:
            raise Exception(
                "Language {} not found in supported languages ({})".format(
                    lang, ", ".join(app.config["SUPPORTED_LOCALES"]
                    )
                )
            )

def static_url_for(*args, **kwargs):
    url = url_for("static", **kwargs)
    if not static_url_exists(url[1:]):
        raise Exception("Static URL {} does not exist".format(url))

    return url

LEAFLET_CSS_FILES = [
    'leaflet/leaflet.css'
]

LEAFLET_JS_FILES = [
    'leaflet/leaflet.js',
    'leaflet/leafletembed.js'
]

JQUERY_FORM_FILES = [
    'jquery_plugins/jquery.form.min.js'
]

DROPZONE_JS_FILES = [
    'dropzone.js'
]

def require_js(filenames):
    if not isinstance(filenames, list):
        filenames = [filenames]
        
    for f in filenames:
        g.js_scripts.append(static_url_for(filename=f))

def require_css(filenames):
    for f in filenames:
        g.css.append(static_url_for(filename=f))

def init_request():
    g.lang = get_locale()
    logger.info("Set request language %s", g.lang)
    session.set("lang", g.lang)
    g.ep_data = {}
    g.js_scripts = []
    g.css = []
    g.translations = get_js_strings()

