{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    <div id="accordion" role="tablist" aria-multiselectable="true">
        {% for category in categories | sort %}
        <div class="card">
            <div class="card-header" role="tab" id="{{category.category_id}}_heading">
                <h3>
                    <a data-toggle="collapse" data-parent="#accordion" href="#{{category.category_id}}_collapse" aria-expanded="true" aria-controls="{{category.category_id}}_collapse">
                        {{ category.category_name}}
                    </a>
                </h3>
            </div>
            <div id="{{category.category_id}}_collapse" class="collapse" role="tabpanel" aria-labelledby="headingOne">
                <div class="card-block">
                    <p><strong>{{category.category_intro}}</strong></p>
                    {% for course in category.courses | sort %}
                        <div>
                            <p><i>{{course.course_name}}</i>: {{course.university_names() | join(", ")}}</p>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

{% endblock %}