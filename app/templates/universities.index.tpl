{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    {% for university in universities | sort %}
    <h3>
        <a href="{{url_for('.render_university', university_id=university.university_id)}}">{{university.university_name}}</a>
    </h3>
    {% endfor %}
    
</div>

{% endblock %}