{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    <h2>{{_("Your Dashboard") }}</h2>
    
    {% if current_user.is_admin() %}
    <div>
        {{ dashboard_macro.render_pending_changes() }}
    </div>
    {% endif %}
    <div class="row">
        <div class="col-sm-6">
            <div id="add_accordion" role="tablist" aria-multiselectable="true">
                <div class="card plain">
                    <div class="card-title" role="tab" id="categories_heading">
                        <h3>
                            <a data-toggle="collapse" data-parent="#add_accordion" href="#add_category_collapse" aria-expanded="true" aria-controls="add_category_collapse">
                            {{_("Add New Category")}}
                            </a>
                        </h3>
                    </div>
                    <div id="add_category_collapse" class="collapse show" role="tabpanel" aria-labelledby="headingOne">
                        <div class="card-block">
                            {{ dashboard_macro.render_add_new_category_form() }}
                        </div>
                    </div>
                </div>

                <div class="card plain">
                    <div class="card-title" role="tab" id="courses_heading">
                        <a data-toggle="collapse" data-parent="#add_accordion" href="courses_collapse" aria-expanded="true" aria-controls="courses_collapse">
                            <h3>{{_("Add Courses")}}</h3>
                        </a>
                    </div>
                </div>
                <div class="card plain">
                    <div class="card-title" role="tab" id="universities_heading">
                        <a data-toggle="collapse" data-parent="#add_accordion" href="universities_collapse" aria-expanded="true" aria-controls="universities_collapse">
                            <h3>{{_("Add Universities")}}</h3>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div id="edit_accordion" role="tablist" aria-multiselectable="true">
                <div class="card plain">
                    <div class="card-title" role="tab" id="categories_heading">
                        <h3>
                            <a data-toggle="collapse" data-parent="#edit_accordion" href="#edit_category_collapse" aria-expanded="true" aria-controls="edit_category_collapse">
                            {{_("Edit Categories")}}
                            </a>
                        </h3>
                    </div>
                    <div id="edit_category_collapse" class="collapse show" role="tabpanel" aria-labelledby="headingOne">
                        {% for id, name in categories %}
                        {{ dashboard_macro.render_edit_category(id, name) }}
                        {% endfor %}
                    </div>
                </div>

                <div class="card plain">
                    <div class="card-title" role="tab" id="courses_heading">
                        <a data-toggle="collapse" data-parent="#edit_accordion" href="courses_collapse" aria-expanded="true" aria-controls="courses_collapse">
                            <h3>{{_("Edit Courses")}}</h3>
                        </a>
                    </div>
                </div>
                <div class="card plain">
                    <div class="card-title" role="tab" id="universities_heading">
                        <a data-toggle="collapse" data-parent="#edit_accordion" href="universities_collapse" aria-expanded="true" aria-controls="universities_collapse">
                            <h3>{{_("Edit Universities")}}</h3>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="{{url_for('static', filename='dashboard.js')}}"></script>
{% endblock %}
