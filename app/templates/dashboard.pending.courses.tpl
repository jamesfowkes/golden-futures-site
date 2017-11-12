{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Pending Changes - Courses")) }}
    {% if current_user.is_admin() %}
    <div class="container">
        <div class="row">
            <div class="col-sm-4">
                {% if pending.additions | length %}
                <h4>{{_("Additions")}}</h4>
                    {% for addition in pending.additions %}
                    <div class="pending">
                        <p><strong>{{_("New Course")}}: {{addition.course_name}}</strong></p>
                        {{dashboard_macro.approve("course", addition.pending_id)}} {{dashboard_macro.reject("course", addition.pending_id)}}
                    </div>
                    {% endfor %}
                {% else %}
                <h4>{{_("No pending additions")}}</h4>
                {% endif %}
            </div>
            <div class="col-sm-4">
                <h4>{{_("Edits")}}</h4>
                {% for edit in edits %}
                <div class="pending">
                    <p><strong>{{_("Edit Course")}}</strong></p>
                    <p>{{_("Old Name")}}: {{edit.old_name}}</p>
                    <p>{{_("New Name")}}: {{ edit.course_name }}</p>
                    {{dashboard_macro.approve("course", edit.pending_id)}} {{dashboard_macro.reject("course", edit.pending_id)}}
                </div>
                {% endfor %}
            </div>
            <div class="col-sm-4">
                <h4>{{_("Deletions")}}</h4>
                {% for deletion in pending.deletions %}
                <div class="pending">
                    <p><strong>{{_("New Course")}}: {{deletion.course_name}}</strong></p>
                    {{dashboard_macro.approve("course", deletion.pending_id)}} {{dashboard_macro.reject("course", deletion.pending_id)}}
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% else %}
    <p>Only admin users may approve pending changes!</p>
    {% endif %}
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
{% endblock %}
