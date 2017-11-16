import logging

import jinja2

from flask import g

from app import app
from app import session
from app.locale import get_locale, get_js_strings

logger = logging.getLogger(__name__)

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

def init_request():
    g.lang = get_locale()
    logger.info("Set request language %s", g.lang)
    session.set("lang", g.lang)
    g.ep_data = {}
    g.translations = get_js_strings()
