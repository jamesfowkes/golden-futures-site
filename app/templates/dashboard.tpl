{% extends "layout.tpl" %}

{% macro approve(type, id) -%}
    <button type="button" approveid="{{id}}" class="approve-{{type}} btn btn-outline-success btn-sm">{{_("Approve")}}</button>
{%- endmacro %}

{% macro reject(type, id) -%}
    <button type="button" rejectid="{{id}}" class="reject-{{type}} btn btn-outline-danger btn-sm">{{_("Reject")}}</button>
{%- endmacro %}

{% macro render_pending_additions(additions) -%}
    {% if additions | length %}
        <div id="additions">
            <h4>{{_("Additions")}}</h4>
            {% for addition in additions["category"] %}
                <span>{{_("New Category")}}: <strong>{{addition}}</strong> {{approve("category", addition.pending_id)}} {{reject("category", addition.pending_id)}}</span>
            {% endfor %}
        </div>
    {% endif %}
{%- endmacro %}

{% macro render_pending_edits(edits) -%}
    {% if edits | length %}
        <div id="edits">
            <h4>{{_("Edits")}}</h4>
            {% for edit in edits["category"] %}
                <span>{{_("Edit Category")}}: <strong>{{edit}}</strong> {{approve("category", edit.pending_id)}} {{reject("category", edit.pending_id)}}</span>
            {% endfor %}
        </div>
    {% endif %}
{%- endmacro %}

{% macro render_pending_deletions(deletions) -%}
    {% if deletions | length %}
        <div id="deletions">
            <h4>{{_("Deletions")}}</h4>
            {% for deletion in deletions["category"] %}
                <span>{{_("Remove Category")}}: <strong>{{deletion}}</strong> {{approve("category", deletion.pending_id)}} {{reject("category", deletion.pending_id)}}</span>
            {% endfor %}
        </div>
    {% endif %}
{%- endmacro %}

{% macro render_pending_changes() -%}
<div class="card plain">
    <div class="card-title" role="tab" id="approval_heading">
        <a data-toggle="collapse" data-parent="#accordion" href="approval_collapse" aria-expanded="true" aria-controls="approval_collapse">
            <h3>{{_("Waiting for Approval")}}</h3>
        </a>
        {{ render_pending_additions(pending.additions) }}
        {{ render_pending_edits(pending.edits) }}
        {{ render_pending_deletions(pending.deletions) }}
    </div>
</div>
{%- endmacro %}

{% macro render_add_new_category_form() -%}
<form>
    <div id="form_add_category" class="form-group" action="{{url_for('create_category')}}"">
        <h4>{{ _("Category Details") }}</h4>
        <label for="category_name" class="sr-only">{{ _("Category Name") }}</label>
        <input class="form-control" type="text" id="category_name" name="category_name" placeholder="Category Name" lang="{{g.lang}}" required>
        <label for="category_intro" class="sr-only">{{ _("Category Introduction") }}</label>
        <input class="form-control" type="text" id="category_intro" name="category_intro" placeholder="Category Introduction" lang="{{g.lang}}" required>
        <label for="category_careers" class="sr-only">{{ _("Category Careers") }}</label>
        <input class="form-control" type="text" id="category_careers" name="category_careers" placeholder="Category Careers" lang="{{g.lang}}" required>
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
