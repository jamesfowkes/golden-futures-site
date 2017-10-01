import logging

import sqlalchemy_i18n
import sqlalchemy_utils
from flask_babel import Babel, gettext

from flask import request, g

from app import app

logger = logging.getLogger(__name__)

babel = Babel()

@babel.localeselector
def get_locale():
    try:
        locale = g.lang
    except:
        try:
            logger.info("No language in g.lang, falling back to request languages")
            locale = request.accept_languages.best_match(app.config["SUPPORTED_LOCALES"])
        except:
            logger.info("No request (not in context?), falling back to 'en'")
            locale = "en"

    return locale
    
def init_app(app):
    babel.init_app(app)
    sqlalchemy_utils.i18n.get_locale = get_locale
    sqlalchemy_i18n.make_translatable(options={'locales': app.config["SUPPORTED_LOCALES"]})
