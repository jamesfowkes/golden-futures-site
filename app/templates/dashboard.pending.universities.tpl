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
                {% for addition in pending.additions %}
                <a href="{{url_for('render_pending_uni_summary', pending_id=addition.pending_id)}}">{{addition.university_name}}</a>
                {% endfor %}
                {% else %}
                <h4>{{_("No pending additions")}}</h4>
                {% endif %}
            </div>
        </div>
        <div class="card-block">
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
        <div class="card-block">
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
    {% else %}
    <p>Only admin users may approve pending changes!</p>
    {% endif %}
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
{% endblock %}
