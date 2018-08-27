{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.category.macro' as dashboard_category_macro with context%}
{% import 'dashboard.course_selector.macro' as dashboard_course_selector_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Category: ") + category.category_name) }}
    <div>
        <div>
            <h4>{{ _("Category Details") }}</h4>
            {{ dashboard_category_macro.render_edit_category_form(category, languages=languages) }}
        </div>
        <div>
            <h4>{{_("Assign Courses")}}</h4>
            <form id="form_edit_category_courses" method="post">
                {{ dashboard_course_selector_macro.render_course_selector(category, all_courses, alphabetised_courses) }}
                <button id="edit_category_courses" class="btn btn-default btn-block" type="button">{{_("Submit")}}</button>
            </form>
        </div>
    </div>

</div>
{% endblock %}

{% block js %}
    {{ super() }}
{% endblock %}
