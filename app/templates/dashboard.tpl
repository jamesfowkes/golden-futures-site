{% extends "layout.tpl" %}

{% macro render_pending_changes() -%}
<div class="card plain">
    <div class="card-title" role="tab" id="approval_heading">
        <a data-toggle="collapse" data-parent="#accordion" href="approval_collapse" aria-expanded="true" aria-controls="approval_collapse">

        <h3>{{_("Waiting for Approval")}}</h3>
    </div>
</div>
{%- endmacro %}

{% macro render_add_new_category_form() -%}
<form>
    <div id="form_add_category" class="form-group">
        <h4>{{ _("Category Details") }}</h4>
        <label for="category_name" class="sr-only">{{ _("Category Name") }}</label>
        <input class="form-control" type="text" id="category_name" name="category_name" placeholder="Category Name" lang="{{g.lang}}" required>
        <label for="category_intro" class="sr-only">{{ _("Category Introduction") }}</label>
        <input class="form-control" type="text" id="category_intro" name="category_intro" placeholder="Category Introduction" lang="{{g.lang}}" required>
        <div id="category_careers">
            <h4>{{_("Add Careers") }}</h4>
        </div>
        <button id="add_career" class="btn btn-default btn-sm" type="button">{{_("Add Career")}}</button>
        <button id="add_category" class="btn btn-default btn-block" type="button">{{_("Submit New Category")}}</button>
    </div>
</form>
{%- endmacro %}

{% macro render_categories() -%}
{%- endmacro %}

{% block content %}
<div class="container">
    <h2>{{_("Your Dashboard") }}</h2>

    <div id="accordion" role="tablist" aria-multiselectable="true">

        {% if current_user.is_admin() %}
        {{ render_pending_changes() }}
        {% endif %}

        <div class="card plain">
            <div class="card-title" role="tab" id="categories_heading">
                <h3>
                    <a data-toggle="collapse" data-parent="#accordion" href="#add_category_collapse" aria-expanded="true" aria-controls="add_category_collapse">
                    {{_("Add New Category")}}
                    </a>
                </h3>
            </div>
            <div id="add_category_collapse" class="collapse show" role="tabpanel" aria-labelledby="headingOne">
                <div class="card-block">
                    {{ render_add_new_category_form() }}
                </div>
            </div>
        </div>

        <div class="card plain">
            <div class="card-title" role="tab" id="courses_heading">
                <a data-toggle="collapse" data-parent="#accordion" href="courses_collapse" aria-expanded="true" aria-controls="courses_collapse">
                    <h3>{{_("Add/Edit Courses")}}</h3>
                </a>
            </div>
        </div>
        <div class="card plain">
            <div class="card-title" role="tab" id="universities_heading">
                <a data-toggle="collapse" data-parent="#accordion" href="universities_collapse" aria-expanded="true" aria-controls="universities_collapse">
                    <h3>{{_("Add/Edit Universities")}}</h3>
                </a>
            </div>
        </div>
</div>

{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
{% endblock %}
