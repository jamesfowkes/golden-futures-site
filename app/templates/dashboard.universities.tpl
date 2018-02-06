{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.university.macro' as dashboard_university_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Universities")) }}

    <div class="row">
        <div class="col-sm-6">
            <div class="card plain">
                <div class="card-title" role="tab" id="universities_heading">
                    <h3 id="add_new_university">{{_("Add New university")}}</h3>
                </div>
                <div aria-labelledby="add_new_university">
                    <div class="card-block">
                        {{ dashboard_university_macro.render_add_new_university_form() }}
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="card plain">
                <div class="card-title" role="tab" id="universities_heading">
                    <h3 id="edit_university">{{_("Edit universities")}}</h3>
                </div>
                <div id="catgories_list" aria-labelledby="edit_university">
                    {% for university in universities %}
                        {% if university.is_pending() %}
                            {{ dashboard_university_macro.render_edit_pending_university_link(university) }}
                        {% else %}
                            {{ dashboard_university_macro.render_edit_university_link(university) }}
                        {% endif %}
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
    <script src="{{url_for('static', filename='dashboard.university.js')}}"></script>
{% endblock %}