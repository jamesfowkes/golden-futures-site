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
from app.blueprints.common import static_url_for, require_js, require_css, JQUERY_FORM_FILES
from app.blueprints.dashboard import dashboard

from app import app
from app import locale

logger = logging.getLogger(__name__)

@dashboard.route("/dashboard/pending/courses", methods=['GET'])
@flask_login.login_required
def render_pending_course_changes():
    require_js('dashboard.js')
    pending_changes = CoursePending.all_by_type()
    return render_template('dashboard.pending.courses.tpl', pending=pending_changes)

@dashboard.route("/dashboard/courses/edit/<course_id>", methods=['GET'])
@flask_login.login_required
def render_edit_course_dashboard(course_id):
    g.ep_data["course_id"] = course_id
    g.ep_data["api_endpoints"] = {"edit_course":url_for("edit_course", course_id=course_id)}

    require_js('dashboard.js')
    require_js('dashboard.course.edit.js')
    require_js(JQUERY_FORM_FILES)

    course = Course.get_single(course_id=course_id)
    return render_template('dashboard.course.edit.tpl',
        course=course,
        languages=locale.supported_languages()
    )

@dashboard.route("/dashboard/courses/editpending/<pending_id>", methods=['GET'])
@flask_login.login_required
def render_edit_pending_course_dashboard(pending_id):
    g.ep_data["pending_id"] = pending_id
    g.ep_data["api_endpoints"] = {"edit_course": url_for("edit_pending_course", pending_id=pending_id)}
    course = CoursePending.get_single(pending_id=pending_id)
    return render_template('dashboard.course.edit.tpl',
        course=course,
        languages=locale.supported_languages()
    )
    
@dashboard.route("/dashboard/courses", methods=['GET'])
@flask_login.login_required
def render_courses_dashboard():
    g.ep_data["api_endpoints"] = {"add_course":url_for("create_course")}

    require_js('dashboard.js')
    require_js('dashboard.course.edit.js')
    require_js(JQUERY_FORM_FILES)

    live_courses = Course.all()
    pending_courses = CoursePending.all()
    pending_courses = list(filter(lambda c: c.is_addition(), pending_courses))

    all_courses = live_courses + pending_courses
    all_courses = sorted(all_courses, key=lambda c: c.course_name[0])
    return render_template('dashboard.courses.tpl',
        courses=all_courses,
        languages=locale.supported_languages()
    )
