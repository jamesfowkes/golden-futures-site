import logging

from collections import defaultdict, OrderedDict

from flask import Blueprint, g, render_template, request, redirect, url_for
import flask_login

from app.models.university import University
from app.models.category import Category, CategoryPending
from app.models.course import Course, CoursePending
from app.models.university import University, UniversityPending

from app.models.pending_changes import PendingChanges

from app.blueprints import common

logger = logging.getLogger(__name__)

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route("/dashboard", methods=['GET'])
@flask_login.login_required
def render_dashboard():
    return render_template('dashboard.tpl')

@dashboard.route("/dashboard/pending/categories", methods=['GET'])
@flask_login.login_required
def render_pending_category_changes():
    pending_changes = CategoryPending.all_by_type()
    return render_template('dashboard.pending.categories.tpl', pending=pending_changes)

@dashboard.route("/dashboard/pending/courses", methods=['GET'])
@flask_login.login_required
def render_pending_course_changes():
    pending_changes = CoursePending.all_by_type()
    return render_template('dashboard.pending.courses.tpl', pending=pending_changes)

@dashboard.route("/dashboard/pending/universities", methods=['GET'])
@flask_login.login_required
def render_pending_university_changes():
    pending_changes = UniversityPending.all_by_type()
    return render_template('dashboard.pending.universities.tpl', pending=pending_changes)

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

@dashboard.route("/dashboard/categories/editpending/<pending_id>", methods=['GET'])
@flask_login.login_required
def render_edit_pending_category_dashboard(pending_id):
    g.ep_data["pending_id"] = pending_id
    g.ep_data["api_endpoint"] = url_for("edit_pending_category", pending_id=pending_id)
    category = CategoryPending.get_single(pending_id=pending_id)
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
    g.ep_data["api_endpoint"] = url_for("edit_course", course_id=course_id)
    course = Course.get_single(course_id=course_id)
    return render_template('dashboard.course.edit.tpl', course=course)

@dashboard.route("/dashboard/courses/editpending/<pending_id>", methods=['GET'])
@flask_login.login_required
def render_edit_pending_course_dashboard(pending_id):
    g.ep_data["pending_id"] = pending_id
    g.ep_data["api_endpoint"] = url_for("edit_pending_course", pending_id=pending_id)
    course = CoursePending.get_single(pending_id=pending_id)
    return render_template('dashboard.course.edit.tpl', course=course)

@dashboard.route("/dashboard/categories", methods=['GET'])
@flask_login.login_required
def render_categories_dashboard():
    live_categories = Category.all()
    pending_categories = CategoryPending.all()
    all_categories = live_categories + pending_categories
    all_categories = sorted(all_categories, key=lambda c: c.category_name[0])
    return render_template('dashboard.categories.tpl', categories=all_categories)
    
@dashboard.route("/dashboard/courses", methods=['GET'])
@flask_login.login_required
def render_courses_dashboard():
    live_courses = Course.all()
    pending_courses = CoursePending.all()
    pending_courses = list(filter(lambda c: c.is_addition(), pending_courses))

    all_courses = live_courses + pending_courses
    all_courses = sorted(all_courses, key=lambda c: c.course_name[0])
    return render_template('dashboard.courses.tpl', courses=all_courses)

@dashboard.route("/dashboard/universities", methods=['GET'])
@flask_login.login_required
def render_universities_dashboard():
    live_universities = University.all()
    pending_universities = UniversityPending.all()
    all_universities = live_universities + pending_universities
    all_universities = sorted(all_universities, key=lambda c: c.university_name[0])
    return render_template('dashboard.universities.tpl', universities=all_universities)

@dashboard.route("/dashboard/universities/edit/<university_id>", methods=['GET'])
@flask_login.login_required
def render_edit_university_dashboard(university_id):
    g.ep_data["university_id"] = university_id
    university = university.get_single(university_id=university_id)
    courses = sorted(Course.all(), key=lambda c: c.course_name)
    alphabetised_courses = defaultdict(list)
    for course in courses:
        first_letter = course.course_name[0]
        alphabetised_courses[first_letter].append(course)

    sorted_alphabetised_courses = OrderedDict(sorted(alphabetised_courses.items()))
    return render_template('dashboard.university.edit.tpl', university=university, all_courses=courses, alphabetised_courses=sorted_alphabetised_courses)

@dashboard.route("/dashboard/universities/editpending/<pending_id>", methods=['GET'])
@flask_login.login_required
def render_edit_pending_university_dashboard(pending_id):
    g.ep_data["pending_id"] = pending_id
    g.ep_data["api_endpoint"] = url_for("edit_pending_university", pending_id=pending_id)
    university = universityPending.get_single(pending_id=pending_id)
    courses = sorted(Course.all(), key=lambda c: c.course_name)
    alphabetised_courses = defaultdict(list)
    for course in courses:
        first_letter = course.course_name[0]
        alphabetised_courses[first_letter].append(course)

    sorted_alphabetised_courses = OrderedDict(sorted(alphabetised_courses.items()))
    return render_template('dashboard.university.edit.tpl', university=university, all_courses=courses, alphabetised_courses=sorted_alphabetised_courses)


def init_app(app):
    dashboard.before_request(common.init_request)
    dashboard.add_app_template_filter(common.language_name)
    app.register_blueprint(dashboard)
