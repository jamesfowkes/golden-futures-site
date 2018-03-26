{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context %}
{% import 'dashboard.mapping.macro' as dashboard_mapping_macro with context %}
{% import 'dashboard.university.macro' as dashboard_university_macro with context %}
{% import 'dashboard.course_selector.macro' as dashboard_course_selector_macro with context %}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage university: ") + university.university_name) }}
    <form id="form_add_university">
        <div id="accordion" role="tablist" aria-multiselectable="true">
            <div class="card plain" role="tab">
                <div class="card-title" role="tab">
                    <h3>
                        <a id="university_nametitle_heading" data-toggle="collapse" href="#university_nametitle_collapse" aria-expanded="true" aria-controls="university_nametitle_collapse">
                        {{ _("Name and Introduction") }}
                        </a>
                    </h3>
                </div>

                <div id="university_nametitle_collapse" class="collapse show" role="tabpanel" aria-labelledby="university_nametitle_heading">
                    <div class="form-group card-block">
                        <div class="row">
                            <div class="col-sm-6">
                            {{ dashboard_university_macro.render_university_fields(
                                university.translations[languages[0].id].university_name,
                                university.translations[languages[0].id].university_intro,
                                languages[0]) }}
                            </div>
                            <div class="col-sm-6">
                            {{ dashboard_university_macro.render_university_fields(
                                university.translations[languages[1].id].university_name,
                                university.translations[languages[1].id].university_intro,
                                languages[1]) }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card plain" role="tab">
                <div class="card-title" role="tab">
                    <h3>
                        <a id="location_selector_heading" data-toggle="collapse" href="#location_selector_collapse" aria-expanded="true" aria-controls="location_selector_collapse">
                        {{_("Location")}}
                        </a>
                    </h3>
                </div>
                <div id="location_selector_collapse" class="collapse" role="tabpanel" aria-labelledby="location_selector_heading">
                    <div class="form-group card-block">
                        {{ dashboard_mapping_macro.render_location_selector() }}
                    </div>
                </div>
            </div>

            <div class="card plain" role="tab">
                <div class="card-title" role="tab">
                    <h3>
                        <a id="contact_details_selector_heading" data-toggle="collapse" href="#contact_details_selector_collapse" aria-expanded="true" aria-controls="contact_details_selector_collapse">
                        {{_("Contact Details")}}
                        </a>
                    </h3>
                </div>
                <div id="contact_details_selector_collapse" class="collapse" role="tabpanel" aria-labelledby="contact_details_selector_heading">
                    <div class="form-group card-block">
                        <h4>{{_("Web Address")}}</h4>
                        <div class="row">
                            <div class="col-sm-6">
                                {{ dashboard_university_macro.render_website_address_editor(university, languages[0]) }}
                            </div>
                            <div class="col-sm-6">
                                {{ dashboard_university_macro.render_website_address_editor(university, languages[1]) }}
                            </div>
                        </div>

                        <h4>{{_("Other Contact Details")}}</h4>
                        <div id="contact_details_container">
                        {{ dashboard_university_macro.render_contact_details_editor(university, languages) }}
                        </div>
                        <button type="button" id="add_new_contact_details" class="btn btn-default btn-block">{{_("Add another")}}</button>
                    </div>
                </div>
            </div>

            <div class="card plain" role="tab">
                <div class="card-title" role="tab">
                    <h3>
                        <a id="course_selector_heading" data-toggle="collapse" href="#course_selector_collapse" aria-expanded="true" aria-controls="course_selector_collapse">
                        {{_("Assign Courses")}}
                        </a>
                    </h3>
                </div>
                <div id="course_selector_collapse" class="collapse" role="tabpanel" aria-labelledby="course_selector_heading">
                    <div class="form-group card-block">
                        {{ dashboard_course_selector_macro.render_course_selector(university, all_courses, alphabetised_courses) }}
                    </div>
                </div>
            </div>

            <div class="card plain" role="tab">
                <div class="card-title" role="tab">
                    <h3>
                        <a id="scholarship_editor_heading" data-toggle="collapse" href="#scholarship_editor_collapse" aria-expanded="true" aria-controls="scholarship_editor_collapse">
                        {{_("Scholarships")}}
                        </a>
                    </h3>
                </div>
                <div id="scholarship_editor_collapse" class="collapse" role="tabpanel" aria-labelledby="scholarship_editor_heading">
                    <div class="form-group card-block">
                        <div class="row">
                            <div class="col-sm-6">
                                {{ dashboard_university_macro.scholarship_editor(university, languages[0]) }}
                            </div>
                            <div class="col-sm-6">
                                {{ dashboard_university_macro.scholarship_editor(university, languages[1]) }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card plain" role="tab">
                <div class="card-title" role="tab">
                    <h3>
                        <a id="facility_editor_heading" data-toggle="collapse" href="#facility_editor_collapse" aria-expanded="true" aria-controls="facility_editor_collapse">
                        {{_("Facilities")}}
                        </a>
                    </h3>
                </div>
                <div id="facility_editor_collapse" class="collapse" role="tabpanel" aria-labelledby="facility_editor_heading">
                    <div class="form-group card-block">
                        <div id="facilities_container">
                        {{ dashboard_university_macro.render_facilities_editor(university, languages) }}
                        </div>
                        <button type="button" id="add_new_facility" class="btn btn-default btn-block">{{_("Add another")}}</button>
                    </div>
                </div>
            </div>
            <button id="university_edit_submit" class="btn btn-default btn-block" type="button">{{_("Submit")}}</button>
        </div>
    </form>

</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.university.edit.js')}}"></script>
{% endblock %}
