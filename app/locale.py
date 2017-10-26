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

@babel.localeselector
def get_locale():

    # If the flask request global already has a language set, use that
    try:
        locale = g.lang
        logger.info("Loaded language %s from flask global", locale)
        return locale
    except:
        pass

    # If there is a URL lang parameter, use that
    locale = request.args.get("lang", None)
    if locale:
        logger.info("Loaded language %s from request URL params", locale)
        return locale

    # Try using the language stored in the session
    session_locale = session.get("lang")
    if session_locale:
        logger.info("Loaded language %s from session", locale)
        return session_locale

    # Try using the language of the logged-in user
    if flask_login.current_user.is_authenticated:
        if flask_login.current_user.lang:
            logger.info("Loaded language %s from logged in user", flask_login.current_user.lang)
            return flask_login.current_user.lang

    # Fall back to using the accept_langauges header
    try:
        header_lang = request.accept_languages.best_match(app.config["SUPPORTED_LOCALES"])
        logger.info("Loaded language %s from accept_languages", header_lang)
        return header_lang
    except:
        # If that fails, fall back to english
        logger.info("Falling back to English")
        return "en"

@app.route('/set_language')
def set_language():
    lang = request.args.get('lang', type=int)
    return

def init_app(app):
    babel.init_app(app)
    sqlalchemy_utils.i18n.get_locale = get_locale
    sqlalchemy_i18n.make_translatable(options={'locales': app.config["SUPPORTED_LOCALES"]})
