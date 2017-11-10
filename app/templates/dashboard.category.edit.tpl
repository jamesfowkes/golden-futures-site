{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.category.macro' as dashboard_category_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Category: ") + category.category_name) }}
    <form>
        <div class="form-group">
            {{ dashboard_category_macro.render_edit_new_category_form(category) }}
        </div>
        <div class="form-group">
            <h3>{{_("Assign Courses")}}</h3>
            {{ dashboard_category_macro.render_course_selector(category, all_courses, alphabetised_courses) }}
        </div>
    </form>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.category.js')}}"></script>
{% endblock %}
