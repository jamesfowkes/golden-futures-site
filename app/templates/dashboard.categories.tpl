{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

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

{% macro render_edit_category(id, name) -%}
    <div class="edit_category">
        <a href="{{url_for('dashboard.render_edit_category_dashboard', id=id)}}" class="edit_category" id='{{id}}'>{{name}}</a>
    </div>
{%- endmacro %}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Categories")) }}

    <div class="row">
        <div class="col-sm-6">
            <div class="card plain">
                <div class="card-title" role="tab" id="categories_heading">
                    <h3 id="add_new_category">{{_("Add New Category")}}</h3>
                </div>
                <div aria-labelledby="add_new_category">
                    <div class="card-block">
                        {{ render_add_new_category_form() }}
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="card plain">
                <div class="card-title" role="tab" id="categories_heading">
                    <h3 id="edit_category">{{_("Edit Categories")}}</h3>
                </div>
                <div id="catgories_list" aria-labelledby="edit_category">
                    {% for id, name in categories %}
                    {{ render_edit_category(id, name) }}
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.category.js')}}"></script>
{% endblock %}
