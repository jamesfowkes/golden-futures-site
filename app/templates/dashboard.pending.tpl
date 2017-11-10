{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Pending Changes")) }}
    {% if current_user.is_admin() %}
    <div id="approval_collapse" class="collapse show">
        {{ dashboard_macro.render_pending_additions(pending.additions) }}
        {{ dashboard_macro.render_pending_edits(pending.edits) }}
        {{ dashboard_macro.render_pending_deletions(pending.deletions) }}
    </div>
    {% else %}
    <p>Only admin users may approve pending changes!</p>
    {% endif %}
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
{% endblock %}
