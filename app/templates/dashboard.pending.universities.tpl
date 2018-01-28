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
                        <p><i>{{_("Scholarships")}}:</i><br/>
                            {% for scholarship in addition.scholarships %}
                                {{ scholarship.scholarship_string }}<br/>
                            {% endfor %}
                        </p>
                        <p><i>{{_("Facilities")}}:</i> {{ addition.facility_names() | join(", ") }}</p>
                        </p>
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
                        <p><strong>{{_("University")}}: {{edit.university.university_name}}</strong></p>
                        {% if edit.university_name != edit.university.university_name %}
                            <p><i>{{_("New Name")}}</i>: {{edit.university_name}}</p>
                        {% endif %}
                        {% if edit.pending_courses | length %}
                            <p><i>{{_("New Courses")}}</i>: {{edit.course_names | join(", ")}}</p>
                        {% endif %}
                        {% if edit.facilities | length %}
                            <p><i>{{_("New Facilities")}}</i>: {{edit.facility_names() | join(", ")}}</p>
                        {% endif %}

                        {% if edit.contact_details | length %}
                            <p><i>{{_("Contact Details")}}:</i><br/>
                                {% for contact_detail in edit.contact_details %}
                                    {{ contact_detail.contact_detail_string }}<br/>
                                {% endfor %}
                            </p>
                        {% endif %}
                        
                        {% if edit.admissions | length %}
                            <p><i>{{_("New Admission")}}:</i>
                                <ul>
                                {% for admission in edit.admissions %}
                                    <li>{{ admission.admission_string }}</li>
                                {% endfor %}
                                </ul>
                            </p>
                        {% endif %}

                        tuition_fees
                        scholarships
                        university
                        {{dashboard_macro.approve("university", edit.pending_id)}} {{dashboard_macro.reject("university", edit.pending_id)}}
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
