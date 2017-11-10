{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}
{% import 'dashboard.category.macro' as dashboard_category_macro with context%}

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
                        {{ dashboard_category_macro.render_add_new_category_form() }}
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
                    {{ dashboard_category_macro.render_edit_category_link(id, name) }}
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
