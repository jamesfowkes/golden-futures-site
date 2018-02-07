{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.university.macro' as dashboard_university_macro with context%}
{% import 'dashboard.course_selector.macro' as dashboard_course_selector_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage university: ") + university.university_name) }}
    <form id="form_add_university">
        <div class="form-group">
            <h4>{{ _("University Details") }}</h4>
            <div class="form-group">
                {{ dashboard_university_macro.university_name_input(university.university_name) }}
                {{ dashboard_university_macro.university_intro_input(university.university_intro) }}
            </div>
            <div class="form-group">
                <h3>{{_("Assign Courses")}}</h3>
                {{ dashboard_course_selector_macro.render_course_selector(university, all_courses, alphabetised_courses) }}
            </div>
            <button id="university_edit_submit" class="btn btn-default btn-block" type="button">{{_("Submit")}}</button>
        </div>
    </form>

</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.university.edit.js')}}"></script>
{% endblock %}
