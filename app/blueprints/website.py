import logging

from flask import Blueprint, g, render_template, request, redirect, url_for
import flask_login

import jinja2

from app import app
from app.locale import get_locale
from app import session

from app.models.university import University
from app.models.category import Category
from app.models.course import Course

from app.models.pending_changes import PendingChanges

logger = logging.getLogger(__name__)

website = Blueprint('website', __name__, template_folder='templates')

@jinja2.contextfilter
@website.app_template_filter()
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

@website.route("/", methods=['GET'])
def render_index():
    g.active="index"
    target_template = "index.tpl"
    return render_template(target_template)

@website.route("/universities", methods=['GET'])
def render_universities():
    g.active="universities"
    all_universities = University.all()
    all_categories = Category.all()
    data = {
        "universities": all_universities,
        "categories": all_categories
    }
    return render_template('universities.index.tpl', data=data)

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

@website.route("/login", methods=['GET'])
def render_login():
    g.active="login"
    return render_template('login.index.tpl')

@website.route("/logout", methods=['GET'])
def logout():
    g.active="logout"
    flask_login.logout_user()
    return redirect(url_for("website.render_index"))

@website.route("/dashboard", methods=['GET'])
@flask_login.login_required
def render_dashboard():
    return render_template('dashboard.tpl')

@website.route("/dashboard/pending", methods=['GET'])
@flask_login.login_required
def render_pending_changes():
    pending_changes = PendingChanges.all()
    return render_template('dashboard.pending.tpl', pending=pending_changes)

@website.route("/dashboard/categories", methods=['GET'])
@flask_login.login_required
def render_categories_dashboard():
    categories = [(category.category_id, category.category_name) for category in Category.all()]
    categories = sorted(categories, key=lambda c: c[1])
    return render_template('dashboard.categories.tpl', categories=categories)

@website.route("/dashboard/courses", methods=['GET'])
@flask_login.login_required
def render_courses_dashboard():
    courses = [(course.course_id, course.course_name) for course in Course.all()]
    courses = sorted(courses, key=lambda c: c[1])
    return render_template('dashboard.courses.tpl', courses=courses)

@website.route("/dashboard/universities", methods=['GET'])
@flask_login.login_required
def render_universities_dashboard():
    universities = [(university.university_id, university.university_name) for university in University.all()]
    universities = sorted(universities, key=lambda c: c[1])
    return render_template('dashboard.universities.tpl', universities=universities)

@website.route("/settings", methods=['GET'])
@flask_login.login_required
def render_user_settings():
    return render_template('user_settings.tpl')

@website.before_request
def init_request():
    g.lang = get_locale()
    logger.info("Set request language %s", g.lang)
    session.set("lang", g.lang)
    g.ep_data = {}
    g.translations = app.translations

def init_app(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.register_blueprint(website)
    