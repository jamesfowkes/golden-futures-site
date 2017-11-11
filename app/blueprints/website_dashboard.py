import logging

from collections import defaultdict, OrderedDict

from flask import Blueprint, g, render_template, request, redirect, url_for
import flask_login

from app.models.university import University
from app.models.category import Category
from app.models.course import Course
from app.models.pending_changes import PendingChanges

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

@dashboard.route("/dashboard/categories/edit/<category_id>", methods=['GET'])
@flask_login.login_required
def render_edit_category_dashboard(category_id):
    g.ep_data["category_id"] = category_id
    category = Category.get_single(category_id=category_id)
    courses = sorted(Course.all(), key=lambda c: c.course_name)
    alphabetised_courses = defaultdict(list)
    for course in courses:
        first_letter = course.course_name[0]
        alphabetised_courses[first_letter].append(course)

    sorted_alphabetised_courses = OrderedDict(sorted(alphabetised_courses.items()))
    return render_template('dashboard.category.edit.tpl', category=category, all_courses=courses, alphabetised_courses=sorted_alphabetised_courses)

@dashboard.route("/dashboard/courses/edit/<course_id>", methods=['GET'])
@flask_login.login_required
def render_edit_course_dashboard(course_id):
    g.ep_data["course_id"] = course_id
    course = Course.get_single(course_id=course_id)
    courses = sorted(Course.all(), key=lambda c: c.course_name)
    return render_template('dashboard.course.edit.tpl', course=course)

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
