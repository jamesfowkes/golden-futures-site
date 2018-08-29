{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context %}
{% import 'dashboard.mapping.macro' as dashboard_mapping_macro with context %}
{% import 'dashboard.university.macro' as dashboard_university_macro with context %}
{% import 'dashboard.course_selector.macro' as dashboard_course_selector_macro with context %}

{% block styles %}
    {{ super() }}
{% endblock %}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage gallery: ") + university.university_name) }}
    <div id="dropzone" class="dropzone dz-message dz-clickable needsclick sortable"></div>
        <form id="form_edit_gallery" method="post" enctype="multipart/form-data">
           <button id="edit_gallery_submit" class="btn btn-default btn-block" type="button">{{_("Submit")}}</button>
        </form>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script>Dropzone.autoDiscover = false;</script>
{% endblock %}
