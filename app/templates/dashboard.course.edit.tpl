{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.course.macro' as dashboard_course_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage course: ") + course.course_name) }}
    <h4>{{ _("Course Details") }}</h4>
    {{ dashboard_course_macro.render_edit_course_form(course, languages) }}
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.course.edit.js')}}"></script>
    <script src="{{url_for('static', filename='jquery_plugins/jquery.form.min.js')}}"></script>
{% endblock %}
