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
from app.blueprints.common import LEAFLET_JS_FILES, LEAFLET_CSS_FILES, JQUERY_FORM_FILES
from app.blueprints.dashboard import dashboard

from app import app
from app import locale

logger = logging.getLogger(__name__)

@dashboard.route("/dashboard/pending/universities", methods=['GET'])
@flask_login.login_required
def render_pending_university_changes():
    require_js('dashboard.js')
    pending_changes = UniversityPending.all_by_type()
    return render_template('dashboard.pending.universities.tpl', pending=pending_changes)

@dashboard.route("/dashboard/universities", methods=['GET'])
@flask_login.login_required
def render_universities_dashboard():

    g.ep_data["api_endpoints"] = {"add_university": url_for("create_university")}
    
    require_js('dashboard.js'),
    require_js('dashboard.university.add.js'),
    require_js(JQUERY_FORM_FILES)

    live_universities = University.all()
    pending_universities = UniversityPending.all()
    pending_universities = list(filter(lambda c: c.is_addition(), pending_universities))
    all_universities = live_universities + pending_universities
    all_universities = sorted(all_universities, key=lambda c: c.university_name[0])
    return render_template('dashboard.universities.tpl',
        universities=all_universities,
        languages=locale.supported_languages()
    )

@dashboard.route("/dashboard/universities/edit/<university_id>", methods=['GET'])
@flask_login.login_required
def render_edit_university_dashboard(university_id):

    university = University.get_single(university_id=university_id)

    g.ep_data["university_id"] = university_id
    g.ep_data["languages"] = locale.supported_languages()
    g.ep_data["latlong"] = university.latlong
    g.ep_data["university_icon_path"] = static_url_for(filename="leaflet/university.svg")
    g.ep_data["api_endpoints"] = {"edit_university": url_for("edit_university",university_id=university_id)}

    require_js([
        'dashboard.js',
        'dashboard.university.edit.js',
        'uni_location_edit.js'
    ])
    
    require_js(LEAFLET_JS_FILES)
    require_js(JQUERY_FORM_FILES)
    require_css(LEAFLET_CSS_FILES)

    courses = sorted(Course.all(), key=lambda c: c.course_name)
    alphabetised_courses = defaultdict(list)
    for course in courses:
        first_letter = course.course_name[0]
        alphabetised_courses[first_letter].append(course)

    sorted_alphabetised_courses = OrderedDict(sorted(alphabetised_courses.items()))
    return render_template('dashboard.university.edit.tpl',
        university=university,
        all_courses=courses,
        alphabetised_courses=sorted_alphabetised_courses,
        languages=locale.supported_languages()
    )

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

@dashboard.route("/dashboard/pending/view/addition/<pending_id>")
@flask_login.login_required
def render_pending_uni_addition(pending_id):
    university = UniversityPending.get_single_by_id(pending_id=pending_id)

    g.ep_data["approve_reject_redirect"] = url_for('dashboard.render_pending_university_changes')
    g.ep_data["pending_id"] = pending_id
    g.ep_data["latlong"] = university.latlong
    g.ep_data["university_icon_path"] = static_url_for(filename="leaflet/university.svg")
    try:
        g.ep_data["osm_url"] = "http://www.openstreetmap.org/?mlat=" + university.lat + "&mlon=" + university.long + "&zoom=14"
    except TypeError:
        g.ep_data["osm_url"] = None

    return render_template('university.index.tpl', university=university)

@dashboard.route("/dashboard/pending/view/edit/<pending_id>")
@flask_login.login_required
def render_pending_uni_edit(pending_id):
    try:
        university = UniversityPending.get_single_by_id(pending_id=pending_id)
    except:
        logger.info("Expected result for pending id %s", pending_id)
        raise

    g.ep_data["approve_reject_redirect"] = url_for('dashboard.render_pending_university_changes')
    g.ep_data["pending_id"] = pending_id
    g.ep_data["latlong"] = university.latlong
    g.ep_data["university_icon_path"] = static_url_for(filename="leaflet/university.svg")
    g.ep_data["osm_url"] = "http://www.openstreetmap.org/?mlat=" + university.lat + "&mlon=" + university.long + "&zoom=14"

    require_js(LEAFLET_JS_FILES)
    require_js('uni_map_embed.js')
    require_js('dashboard.university.approve.js')
    require_css(LEAFLET_CSS_FILES)

    return render_template('university.index.tpl', university=university)

def init_app(app):
    dashboard.before_request(common.init_request)
    dashboard.add_app_template_filter(common.language_name)
    app.register_blueprint(dashboard)
