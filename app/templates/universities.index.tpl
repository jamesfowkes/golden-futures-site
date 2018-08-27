{% extends "layout.tpl" %}

{% block content %}
<div class="container">

    <div class="card plain" id="filtering">
        <h4 class="card-title">Search and Filter</h4>
        <div class="card-body">
            <div class="filter_controls">
                <label class="label label-default" for="course_filter_dropdown">{{ _("Filter by Category") }}:</label>
                <div class="dropdown" id="course_filter_dropdown">
                    <button class="btn btn-default dropdown-toggle" type="button" id="course_filter_btn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {{ _("Select Category") }}
                    </button>
                    <div class="dropdown-menu" aria-labelledby="course_filter_btn">
                        {% for category in data["categories"] | sort %}
                            <a class="dropdown-item category_filter_button" id="{{ category.category_id }}" href="#">
                                {{ category.category_name }}
                            </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
            <div class="filter_controls">
                <div>
                    <label class="label label-default" for="fee_filter">{{ _("Maximum Tuition Fee") }}:</label>
                </div>
                <input class="input" id="fee_filter"></input>
                <button class="btn btn-default" type="button" id="apply_fee_filter_button">{{ _("Apply") }}</button>
            </div>
            <div>
                <div id="applied_filters"></div>
                <div>
                    <button class="btn btn-default" type="button" style="display:none;" id="reset_all_filter_button">{{ _("Reset Filters") }}</button>
                </div>
            </div>
        </div>
    </div>

    <div class="card plain">
        <div class="card-title" role="tab" id="map_collapse_heading">
            <h3><a data-toggle="collapse" data-parent="#accordion" href="#map_collapse" aria-expanded="true" aria-controls="map_collapse">{{_("Show on Map")}}</a></h3>
        </div>
        <div id="map_collapse" class="collapse">
            <div id="map"></div>
            <a href="#" id="open_map_link">{{_("Open map in new window")}}</a>
        </div>
    </div>

    {% for university in data["universities"] | sort %}
    <div class="card plain university_card"
    category_id="{% for category in university.categories() %}category_{{category.category_id}}|{% endfor %}"
    max_fee="{{ university.maximum_fee() }}"
    min_fee="{{ university.minimum_fee() }}"
    id="{{ university.university_id }}"
    >
        <h4 class="card-title">
            <a class=".card-link", href="{{url_for('.render_university', university_id=university.university_id)}}">{{university.university_name}}</a>
        </h4>
        <div class="card-body">
            {% for tuition_fee in university.tuition_fees %}
            <p class="card-text">{{ tuition_fee }}</p>
            {% endfor %}
            <p class="card-text courses">
            Courses:
                {% for course in university.courses -%}
                <span class="course category_span"
                category_id="{% for category in university.categories() %}category_{{category.category_id}}|{% endfor %}">
                    {{course.course_name}}{% if not loop.last %}<span class="comma">,</span>{% endif %}
                </span>
                {%- endfor %}
            </p>
        </div>
    </div>
    {% endfor %}
    
</div>

{% endblock %}

{% block js %}
    {{ super() }}
{% endblock %}
