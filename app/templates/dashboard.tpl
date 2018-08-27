{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    <h2>{{_("Your Dashboard") }}</h2>
    
    {% if current_user.is_admin() %}
    <div>
        <a href="{{ url_for('dashboard.render_pending_category_changes') }}">{{_("See pending category changes")}}</a>
    </div>
    <div>
        <a href="{{ url_for('dashboard.render_pending_course_changes') }}">{{_("See pending course changes")}}</a>
    </div>
    <div>
        <a href="{{ url_for('dashboard.render_pending_university_changes') }}">{{_("See pending university changes")}}</a>
    </div>
    {% endif %}
    <div>
        <a href="{{ url_for('dashboard.render_categories_dashboard') }}">{{_("Manage categories")}}</a>
    </div>
    <div>
        <a href="{{ url_for('dashboard.render_courses_dashboard') }}">{{_("Manage courses")}}</a>
    </div>
    <div>
        <a href="{{ url_for('dashboard.render_universities_dashboard') }}">{{_("Manage universities")}}</a>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
{% endblock %}
