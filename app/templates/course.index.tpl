{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    <div id="accordion" role="tablist" aria-multiselectable="true">
        {% for category in categories | sort %}
        <div class="card plain">
            <div class="card-title" role="tab" id="{{category.category_id}}_heading">
                <h3>
                    <a data-toggle="collapse" data-parent="#accordion" href="#{{category.category_id}}_collapse" aria-expanded="true" aria-controls="{{category.category_id}}_collapse">
                        {{ category.category_name}}
                    </a>
                </h3>
            </div>
            <div id="{{category.category_id}}_collapse" class="collapse" role="tabpanel" aria-labelledby="headingOne">
                <div class="card-block">
                    <p><strong>{{category.category_intro}}</strong></p>
                    <p><strong>{{_("Careers")}}</strong>: {{category.category_careers}}</p>
                    <p><strong>{{_("Courses and Universities:")}}</strong></p>
                    {% for course in category.courses | sort %}
                        <div>
                            <p><i>{{course.course_name}}</i>:
                            {% for university in course.universities %}
                                <a href="{{url_for('.render_university', university_id=university.university_id)}}">{{university.university_name}}</a>{% if not loop.last %},{% endif %}
                            {% endfor %}
                            </p>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

{% endblock %}