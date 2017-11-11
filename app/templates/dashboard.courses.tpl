{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.course.macro' as dashboard_course_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Courses")) }}

    <div class="row">
        <div class="col-sm-6">
            <div class="card plain">
                <div class="card-title" role="tab" id="courses_heading">
                    <h3 id="add_new_category">{{_("Add New Course")}}</h3>
                </div>
                <div aria-labelledby="add_new_course">
                    <div class="card-block">
                        {{ dashboard_course_macro.render_add_new_course_form() }}
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="card plain">
                <div class="card-title" role="tab" id="courses_heading">
                    <h3 id="edit_course">{{_("Edit Courses")}}</h3>
                </div>
                <div id="catgories_list" aria-labelledby="edit_course">
                    {% for id, name in courses %}
                    {{ dashboard_course_macro.render_edit_course_link(id, name) }}
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.course.js')}}"></script>
{% endblock %}
