import logging

from flask import Blueprint, g, render_template, request, redirect, url_for
import flask_login

from app.models.university import University
from app.models.category import Category
from app.models.course import Course

from app.blueprints import common

logger = logging.getLogger(__name__)

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route("/dashboard", methods=['GET'])
@flask_login.login_required
def render_dashboard():
    return render_template('dashboard.tpl')

@dashboard.route("/dashboard/pending", methods=['GET'])
@flask_login.login_required
def render_pending_changes():
    pending_changes = PendingChanges.all()
    return render_template('dashboard.pending.tpl', pending=pending_changes)

@dashboard.route("/dashboard/categories/edit/<id>", methods=['GET'])
@flask_login.login_required
def render_edit_category_dashboard(id):
    g.ep_data["id"] = id
    category = Category.get_single(category_id=id)
    return render_template('dashboard.category.edit.tpl', category=category)

@dashboard.route("/dashboard/categories", methods=['GET'])
@flask_login.login_required
def render_categories_dashboard():
    categories = [(category.category_id, category.category_name) for category in Category.all()]
    categories = sorted(categories, key=lambda c: c[1])
    return render_template('dashboard.categories.tpl', categories=categories)
    
@dashboard.route("/dashboard/courses", methods=['GET'])
@flask_login.login_required
def render_courses_dashboard():
    courses = [(course.course_id, course.course_name) for course in Course.all()]
    courses = sorted(courses, key=lambda c: c[1])
    return render_template('dashboard.courses.tpl', courses=courses)

@dashboard.route("/dashboard/universities", methods=['GET'])
@flask_login.login_required
def render_universities_dashboard():
    universities = [(university.university_id, university.university_name) for university in University.all()]
    universities = sorted(universities, key=lambda c: c[1])
    return render_template('dashboard.universities.tpl', universities=universities)

def init_app(app):
    dashboard.before_request(common.init_request)
    dashboard.add_app_template_filter(common.language_name)
    app.register_blueprint(dashboard)
    