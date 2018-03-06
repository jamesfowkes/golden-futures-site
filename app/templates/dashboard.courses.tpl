{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.course.macro' as dashboard_course_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Courses")) }}

    <div class="card plain">
        <div class="card-title" role="tab" id="courses_heading">
            <h3 id="add_new_course">{{_("Add New Course")}}</h3>
        </div>
        <div aria-labelledby="add_new_course">
            <div class="card-block">
                <div class="container">
                    {{ dashboard_course_macro.render_add_new_course_form(languages) }}
                </div>
            </div>
        </div>
    </div>

    <div class="card plain">
        <div class="card-title" role="tab" id="courses_heading">
            <h3 id="edit_course">{{_("Edit Courses")}}</h3>
        </div>
        <div id="courses_list" aria-labelledby="edit_course">
            {% for course in courses %}
                {% if course.is_pending() %}
                    Pending
                    {{ dashboard_course_macro.render_edit_pending_course_link(course.pending_id, course.course_name) }}
                {% else %}
                    {{ dashboard_course_macro.render_edit_course_link(course) }}
                {% endif %}
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.course.js')}}"></script>
    <script src="{{url_for('static', filename='jquery_plugins/jquery.form.min.js')}}"></script>
{% endblock %}
