import logging

from collections import defaultdict, OrderedDict

from flask import Blueprint, g, render_template, request, redirect, abort, url_for
import flask_login

from app.models.university import University
from app.models.category import Category, CategoryPending
from app.models.course import Course, CoursePending
from app.models.university import University, UniversityPending

from app.models.pending_changes import PendingChanges

from app.blueprints import common
from app.blueprints.common import static_url_for, require_js, require_css

from app import app
from app import locale

logger = logging.getLogger(__name__)

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route("/dashboard", methods=['GET'])
@flask_login.login_required
def render_dashboard():
    require_js('dashboard.js')
    return render_template('dashboard.tpl')

def init_app(app):
    dashboard.before_request(common.init_request)
    dashboard.add_app_template_filter(common.language_name)
    app.register_blueprint(dashboard)
