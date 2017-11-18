{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Pending Changes - Universities")) }}
    {% if current_user.is_admin() %}
    <div class="container">
        <div class="row">
            <div class="col-sm-4">
                {% if pending.additions | length %}
                <h4 class="pending_heading" i18n_key="pending_add_heading">{{_("Additions")}}</h4>
                    {% for addition in pending.additions %}
                    <div class="pending">
                        <p><strong>{{_("New University")}}: {{addition.university_name}}</strong></p>
                        <p><i>{{_("Introduction")}}:</i> {{addition.university_intro}}</p>
                        <p><i>{{_("Courses")}}:</i> {{ addition.course_names | join(", ") }}</p>
                        <p><i>{{_("Fees")}}:</i> {{ addition.tuition_fees | join(", ") }}</p>
                        <p><i>{{_("Admission")}}:</i>
                            <ul>
                            {% for admission in addition.admissions %}
                                <li>{{ admission.admission_string }}</li>
                            {% endfor %}
                            </ul>
                        </p>
                        <p><i>{{_("Contact Details")}}:</i><br/>
                            {% for contact_detail in addition.contact_details %}
                                {{ contact_detail.contact_detail_string }}<br/>
                            {% endfor %}
                        </p>
                    </div>
                    <div>
                        {{dashboard_macro.approve("university", addition.pending_id)}} {{dashboard_macro.reject("university", addition.pending_id)}} 
                    </div>
                    {% endfor %}
                {% else %}
                <h4>{{_("No pending additions")}}</h4>
                {% endif %}
            </div>
            <div class="col-sm-4">
                {% if pending.edits | length %}
                    <h4 class="pending_heading" i18n_key="pending_edit_heading">{{_("Edits")}}</h4>
                    {% for edit in pending.edits %}
                    <div class="pending">
                        
                    </div>
                    {% endfor %}
                {% else %}
                <h4>{{_("No pending edits")}}</h4>
                {% endif %}
            </div>
            <div class="col-sm-4">
                {% if pending.deletions | length %}
                    <h4 class="pending_heading" i18n_key="pending_del_heading">{{_("Deletions")}}</h4>
                    {% for deletion in pending.deletions %}
                    <div class="pending">
                        
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
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
{% endblock %}
