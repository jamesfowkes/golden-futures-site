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
                        
                        {% if addition.tuition_fees | length %}
                        <p><i>{{_("Fees")}}:</i></p>
                        <ul>
                            {% for fee in addition.tuition_fees %}
                                <li>{{ fee }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}

                        {% if addition.quotes | length %}
                        <p><i>{{_("Quotes")}}:</i></p>
                        <ul>
                        {% for quote in addition.quotes %}
                            <li>{{ quote.quote_string }}</li>
                        {% endfor %}
                        </ul>
                        {% endif %}

                        {% if addition.admissions | length %}
                        <p><i>{{_("Admissions")}}:</i></p>
                        <ul>
                        {% for admission in addition.admissions %}
                            <li>{{ admission.admission_string }}</li>
                        {% endfor %}
                        </ul>
                        {% endif %}

                        {% if addition.contact_details | length %}
                        <p><i>{{_("Contact Details")}}:</i><br/>
                            {% for contact_detail in addition.contact_details %}
                                {{ contact_detail.contact_detail_string }}<br/>
                            {% endfor %}
                        </p>
                        {% endif %}

                        {% if addition.scholarships | length %}
                        <p><i>{{_("Scholarships")}}:</i><br/>
                            {% for scholarship in addition.scholarships %}
                                {{ scholarship.scholarship_string }}<br/>
                            {% endfor %}
                        </p>
                        {% endif %}

                        {% if addition.facilities | length %}                        
                        <p><i>{{_("Facilities")}}:</i> {{ addition.facility_names() | join(", ") }}</p>
                        </p>
                        {% endif %}

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
                            <p><i>{{_("Name")}}</i>: {{edit.university_name}}</p>
                        {% endif %}

                        {% if edit.university_intro != edit.university.university_intro %}
                            <p><i>{{_("Introduction")}}</i>: {{edit.university_intro}}</p>
                        {% endif %}

                        {% if edit.pending_courses | length %}
                            <p><i>{{_("Courses")}}</i>: {{edit.course_names | join(", ")}}</p>
                        {% endif %}

                        {% if edit.tuition_fees | length %}
                            <p><i>{{_("Fees")}}:</i></p>
                            <ul>
                            {% for fee in edit.tuition_fees %}
                                <li>{{ fee }}</li>
                            {% endfor %}
                            </ul>
                        {% endif %}

                        {% if edit.quotes | length %}
                            <p><i>{{_("Quotes")}}:</i></p>
                            <ul>
                            {% for quote in edit.quotes %}
                                <li>{{ quote.quote_string }}</li>
                            {% endfor %}
                            </ul>
                        {% endif %}

                        {% if edit.admissions | length %}
                            <p><i>{{_("Admissions")}}:</i></p>
                            <ul>
                            {% for admission in edit.admissions %}
                                <li>{{ admission.admission_string }}</li>
                            {% endfor %}
                            </ul>
                        {% endif %}

                        {% if edit.contact_details | length %}
                            <p><i>{{_("Contact Details")}}:</i>
                            {% for contact_detail in edit.contact_details %}
                                {{ contact_detail.contact_detail_string }}<br/>
                            {% endfor %}
                            </p>
                        {% endif %}

                        {% if edit.scholarships | length %}
                            <p><i>{{_("Scholarships")}}:</i></p>
                            <ul>
                            {% for scholarship in edit.scholarships %}
                                <li>{{ scholarship.scholarship_string }}</li>
                            {% endfor %}
                            </ul>
                        {% endif %} 

                        {% if edit.facilities | length %}
                            <p><i>{{_("Facilities")}}</i>: {{edit.facility_names() | join(", ")}}</p>
                        {% endif %}

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
