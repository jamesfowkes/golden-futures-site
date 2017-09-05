import sqlalchemy_i18n
import sqlalchemy_utils
from flask_babel import Babel

from flask import request, g

from app import app

babel = Babel()

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["SUPPORTED_LOCALES"])

def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in app.config["SUPPORTED_LOCALES"]:
            g.current_lang = 'en'
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')
    else:
        g.current_lang = 'en'
    
def init_app(app):
    #app.before_request(before)
    babel.init_app(app)
    sqlalchemy_utils.i18n.get_locale = get_locale
    sqlalchemy_i18n.make_translatable(options={'locales': app.config["SUPPORTED_LOCALES"]})