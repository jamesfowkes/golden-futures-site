from sqlalchemy_i18n import make_translatable
import sqlalchemy_utils
from flask_babel import Babel, get_locale

def init_models(app):
    Babel(app)
    sqlalchemy_utils.i18n.get_locale = get_locale
    make_translatable(options={'locales': app.config["SUPPORTED_LOCALES"]})
