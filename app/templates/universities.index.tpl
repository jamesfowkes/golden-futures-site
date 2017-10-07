{% extends "layout.tpl" %}

{% block content %}
<div class="container">

    <div class="card plain" id="filtering">
        <h4 class="card-title">Search and Filter</h4>
        <div class="card-body">
            <div class="btn-group">
                <div class="dropdown" id="course_filter_dropdown">
                    <button class="btn btn-default dropdown-toggle" type="button" id="course_filter_btn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {{ _("Filter by course") }}
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
            <div class="btn-group">
                <button class="btn btn-default" type="button" id="reset_filter_button">{{ _("Reset") }}</button>
            </div>
        </div>
    </div>

    {% for university in data["universities"] | sort %}
    <div class="card plain university_card {% for category in university.categories() %} category_{{category.category_id}} {% endfor %}">
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
                <span class="course category_span {% for category in course.categories%} category_{{category.category_id}} {% endfor %}">
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
    <script src="{{url_for('static', filename='course_filter.js')}}"></script>
{% endblock %}
