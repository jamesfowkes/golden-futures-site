{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.category.macro' as dashboard_category_macro with context%}

{% block content %}
<div class="container">
    {{ dashboard_macro.dashboard_heading(_("Manage Categories")) }}

    <div class="card plain">
        <div class="card-title" role="tab" id="categories_heading">
            <h3 id="add_new_category">{{_("Add New Category")}}</h3>
        </div>
        <div aria-labelledby="add_new_category">
            <div class="card-block">
                <div class="container">
                    <h4>{{ _("Category Details") }}</h4>
                    {{ dashboard_category_macro.render_add_new_category_form(languages) }}
                </div>
            </div>
        </div>
    </div>
    <div class="card plain">
        <div class="card-title" role="tab" id="categories_heading">
            <h3 id="edit_category">{{_("Edit Categories")}}</h3>
        </div>
        <div id="categories_list" aria-labelledby="edit_category">
            {% for category in categories %}
                {% if category.is_pending() %}
                    {{ dashboard_category_macro.render_edit_pending_category_link(category) }}
                {% else %}
                    {{ dashboard_category_macro.render_edit_category_link(category) }}
                {% endif %}
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
    <script src="{{url_for('static', filename='dashboard.category.js')}}"></script>
    <script src="{{url_for('static', filename='jquery_plugins/jquery.form.min.js')}}"></script>
{% endblock %}
