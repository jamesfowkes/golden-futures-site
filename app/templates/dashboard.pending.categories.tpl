{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Pending Changes - Categories")) }}
    {% if current_user.is_admin() %}
    <div class="container">
        <div class="row">
            <div class="col-sm-4">
                {% if pending.additions | length %}
                <h4>{{_("Additions")}}</h4>
                    {% for addition in pending.additions %}
                    <div class="pending">
                        <p><strong>{{_("New Category")}}: {{addition}}</strong></p>
                        <p>{{_("Introduction")}}: {{ addition.category_intro }}</p>
                        <p>{{_("Careers")}}: {{ addition.category_careers }}</p>
                        {% if addition.course_count() %}
                        <p>{{_("Courses")}}: {{ addition.course_names() | join(", ") }}</p>
                        {% endif %}
                        {{dashboard_macro.approve("category", addition.pending_id)}} {{dashboard_macro.reject("category", addition.pending_id)}}
                    </div>
                    {% endfor %}
                {% else %}
                <h4>{{_("No pending additions")}}</h4>
                {% endif %}
            </div>
            <div class="col-sm-4">
                {% if pending.edits | length %}
                    <h4>{{_("Edits")}}</h4>
                    {% for edit in pending.edits %}
                    <div class="pending">
                        <p><strong>{{_("Edit Category")}}: {{edit}}</strong></p>
                        <p>{{_("Introduction")}}: {{edit.category_intro}}</p>
                        <p>{{_("Careers")}}: {{ edit.category_careers }}</p>
                        {% if edit.course_count() %}
                        <p>{{_("Courses")}}: {{ edit.course_names() | join(", ") }}</p>
                        {% endif %}
                        {{dashboard_macro.approve("category", edit.pending_id)}} {{dashboard_macro.reject("category", edit.pending_id)}}
                    </div>
                    {% endfor %}
                {% else %}
                <h4>{{_("No pending edits")}}</h4>
                {% endif %}
            </div>
            <div class="col-sm-4">
                {% if pending.deletions | length %}
                    <h4>{{_("Deletions")}}</h4>
                    {% for deletion in pending.deletions %}
                    <div class="pending">
                        <p><strong>{{_("Remove Category")}}: {{deletion}}</strong></p>
                        {{dashboard_macro.approve("category", deletion.pending_id)}} {{dashboard_macro.reject("category", deletion.pending_id)}}
                    </div>
                    {% endfor %}
                {% else %}
                    <h4>{{_("No pending deletions")}}</h4>
                {% endif %}
            </div>
        </div>
    </div>
    {% else %}
    <p>Only admin users may approve pending changes!</p>
    {% endif %}
{% endblock %}

{% block js %}
    {{ super() }}
{% endblock %}
