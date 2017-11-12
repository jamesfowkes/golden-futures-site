{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.course.macro' as dashboard_course_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage course: ") + course.course_name) }}
    <form id="form_add_course">
        <div class="form-group">
            <h4>{{ _("Course Details") }}</h4>
            <div class="form-group">
                {{ dashboard_course_macro.course_name_input(course.course_name) }}
            <button id="course_edit_submit" class="btn btn-default btn-block" type="button">{{_("Submit")}}</button>
        </div>
    </form>

</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.course.edit.js')}}"></script>
{% endblock %}
