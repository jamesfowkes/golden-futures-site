{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Pending Changes - Universities")) }}
    {% if current_user.is_admin() %}
    <div class="container">
        <div class="card plain">
            <div class="card-title" role="tab">
                <h4 class="pending_heading" i18n_key="pending_edit_heading">{{_("Additions")}}</h4>
            </div>
            <div class="card-block">
                {% if pending.additions | length %}
                <ul>
                    {% for addition in pending.additions %}
                    <li><a href="{{url_for('dashboard.render_pending_uni_addition', pending_id=addition.pending_id)}}">{{addition.university_name}}</a></li>
                    {% endfor %}
                <uli>
                {% else %}
                <h4>{{_("No pending additions")}}</h4>
                {% endif %}
            </div>
        </div>

        <div class="card plain">
            <div class="card-title" role="tab">
                <h4 class="pending_heading" i18n_key="pending_edit_heading">{{_("Edits")}}</h4>
            </div>
            <div class="card-block">
                {% if pending.edits | length %}
                <ul>
                    {% for edit in pending.edits %}
                    <li><a href="{{url_for('dashboard.render_pending_uni_edit', pending_id=edit.pending_id)}}">{{edit.university_name}}</a></li>
                    {% endfor %}
                </ul>
                {% else %}
                <h4>{{_("No pending edits")}}</h4>
                {% endif %}
            </div>
        </div>

        {% if ALLOW_UNIVERSITY_DELETION %}
        <div class="card plain">
            <div class="card-title" role="tab">
                <h4 class="pending_heading" i18n_key="pending_delete_heading">{{_("Deletes")}}</h4>
            </div>
            <div class="card-block">
                {% if pending.deletions | length %}
                <ul>
                {% for delete in pending.deletions %}
                <li>{{_("Delete university ")}}{{ delete.university_name}}</li>
                {% endfor %}
                </ul>
                {% else %}
                <h4>{{_("No pending deletions")}}</h4>
                {% endif %}
            </div>
        </div>
        {% endif %}

    </div>
    {% else %}
    <p>Only admin users may approve pending changes!</p>
    {% endif %}
{% endblock %}

{% block js %}
    {{ super() }}
{% endblock %}
