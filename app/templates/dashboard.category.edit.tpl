{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.category.macro' as dashboard_category_macro with context%}
{% import 'dashboard.course_selector.macro' as dashboard_course_selector_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Category: ") + category.category_name) }}
    <form id="form_add_category">
        <div class="form-group">
            <h4>{{ _("Category Details") }}</h4>
            <div class="form-group">
                {{ dashboard_category_macro.category_name_input(category.category_name) }}
                {{ dashboard_category_macro.category_intro_input(category.category_intro) }}
                {{ dashboard_category_macro.category_careers_input(category.category_careers) }}
            </div>
            <div class="form-group">
                <h3>{{_("Assign Courses")}}</h3>
                {{ dashboard_course_selector_macro.render_course_selector(category, all_courses, alphabetised_courses) }}
            </div>
            <button id="category_edit_submit" class="btn btn-default btn-block" type="button">{{_("Submit")}}</button>
        </div>
    </form>

</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.category.edit.js')}}"></script>
{% endblock %}
