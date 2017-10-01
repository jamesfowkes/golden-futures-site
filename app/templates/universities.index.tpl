{% extends "layout.tpl" %}

{% block content %}
<div class="container">

    <div id="filtering">
    </div>

    {% for university in universities | sort %}
    <div class="card plain">
        <h4 class="card-title">
            <a class=".card-link", href="{{url_for('.render_university', university_id=university.university_id)}}">{{university.university_name}}</a>
        </h4>
        <div class="card-body">
            {% for tuition_fee in university.tuition_fees %}
            <p class="card-text">{{ tuition_fee }}</p>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
    
</div>

{% endblock %}