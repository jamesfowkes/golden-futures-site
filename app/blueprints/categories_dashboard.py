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
from app.blueprints.common import static_url_for, require_js
from app.blueprints.dashboard import dashboard

from app import app
from app import locale

logger = logging.getLogger(__name__)

@dashboard.route("/dashboard/pending/categories", methods=['GET'])
@flask_login.login_required
def render_pending_category_changes():
    require_js('dashboard.js')
    pending_changes = CategoryPending.all_by_type()
    return render_template('dashboard.pending.categories.tpl', pending=pending_changes)

@dashboard.route("/dashboard/categories/edit/<category_id>", methods=['GET'])
@flask_login.login_required
def render_edit_category_dashboard(category_id):
    g.ep_data["category_id"] = category_id
    g.ep_data["api_endpoints"] = {
        "edit_category": url_for("edit_category", category_id=category_id),
        "edit_category_courses": url_for("edit_category_courses", category_id=category_id)
    }

    require_js('dashboard.js')
    require_js('dashboard.category.edit.js')
    
    category = Category.get_single(category_id=category_id)
    courses = sorted(Course.all(), key=lambda c: c.course_name)
    alphabetised_courses = defaultdict(list)
    for course in courses:
        first_letter = course.course_name[0]
        alphabetised_courses[first_letter].append(course)

    sorted_alphabetised_courses = OrderedDict(sorted(alphabetised_courses.items()))
    return render_template(
        'dashboard.category.edit.tpl',
        category=category, all_courses=courses, alphabetised_courses=sorted_alphabetised_courses,
        languages=locale.supported_languages()
    )

@dashboard.route("/dashboard/categories/editpending/<pending_id>", methods=['GET'])
@flask_login.login_required
def render_edit_pending_category_dashboard(pending_id):
    
    g.ep_data["pending_id"] = pending_id
    g.ep_data["api_endpoints"] = {
        "edit_category": url_for("edit_pending_category", pending_id=pending_id),
        "edit_category_courses": url_for("edit_pending_category_courses", pending_id=pending_id)
    }

    category = CategoryPending.get_single(pending_id=pending_id)

    courses = sorted(Course.all(), key=lambda c: c.course_name)
    alphabetised_courses = defaultdict(list)
    for course in courses:
        first_letter = course.course_name[0]
        alphabetised_courses[first_letter].append(course)

    sorted_alphabetised_courses = OrderedDict(sorted(alphabetised_courses.items()))
    return render_template('dashboard.category.edit.tpl',
        category=category, all_courses=courses, alphabetised_courses=sorted_alphabetised_courses,
        languages=locale.supported_languages()
    )

@dashboard.route("/dashboard/categories", methods=['GET'])
@flask_login.login_required
def render_categories_dashboard():

    require_js('dashboard.js')
    require_js('dashboard.category.js')
    require_js('jquery_plugins/jquery.form.min.js')

    live_categories = Category.all()
    pending_categories = CategoryPending.all()
    pending_categories = list(filter(lambda c: c.is_addition(), pending_categories))
    all_categories = live_categories + pending_categories
    all_categories = sorted(all_categories, key=lambda c: c.category_name[0])
    return render_template('dashboard.categories.tpl',
        categories=all_categories,
        languages=locale.supported_languages()
    )
