from collections import namedtuple
import logging

import sqlalchemy_i18n
import sqlalchemy_utils
from flask_babel import Babel, gettext

from flask import request, g
import flask_login

from app import app
from app import session

logger = logging.getLogger(__name__)

babel = Babel()

testing_get_locale = None

Language = namedtuple("Language", ["id", "name"])

@babel.localeselector
def get_locale():

    # If testing, defer to the testing handler
    if app.config["TESTING"] and testing_get_locale:
        return testing_get_locale()
        
    # If the flask request global already has a language set, use that
    try:
        locale = g.lang
        #logger.info("Loaded language %s from flask global", locale)
        return locale
    except:
        pass

    # If there is a URL lang parameter, use that
    try:
        locale = request.args.get("lang", None)
        if locale:
            logger.info("Loaded language %s from request URL params", locale)
            return locale
    except RuntimeError:
        pass #Not in request context, which is fine - just skip this

    # Try using the language stored in the session
    try:
        session_locale = session.get("lang")
        if session_locale is not None:
            logger.info("Loaded language %s from session", session_locale)
            return session_locale
    except RuntimeError:
        pass #Not in request context, which is fine - just skip this

    # Try using the language of the logged-in user
    if flask_login.current_user and flask_login.current_user.is_authenticated and flask_login.current_user.lang:
        logger.info("Loaded language %s from logged in user %s", flask_login.current_user.lang, flask_login.current_user.username)
        return flask_login.current_user.lang

    # Fall back to using the accept_langauges header
    try:
        header_lang = request.accept_languages.best_match(app.config["SUPPORTED_LOCALES"])
        if header_lang:
            logger.info("Loaded language %s from accept_languages", header_lang)
            return header_lang
        else:
            pass
    except:
        pass

    # If all else fails, fall back to english
    logger.info("Falling back to English")
    return "en"

def set_testing_language_selector(selector):
    global testing_get_locale
    testing_get_locale = selector

def init_app(app):
    babel.init_app(app)
    sqlalchemy_utils.i18n.get_locale = get_locale
    sqlalchemy_i18n.make_translatable(options={'locales': app.config["SUPPORTED_LOCALES"]})

    logger.setLevel(logging.WARNING)
    
def supported_languages():
    return [Language(k, v) for k,v in app.config["SUPPORTED_LOCALES"].items()]

def get_js_strings():
    return {
        "add_success": gettext("added successfully"),
        "edit_success": gettext("edited successfully"),
        "pending_add_heading": gettext("No pending additions"),
        "pending_edit_heading": gettext("No pending edits"),
        "pending_del_heading": gettext("No pending deletions"),
        "category_filter_display_text": gettext("Category"),
        "fee_filter_display_text": gettext("Maximum Tuition Fee"),
        "applied_filters": gettext("Applied Filters"),
        "currency": gettext("$"),
        "include_in_filter":  gettext("Include in Filter?")
    }