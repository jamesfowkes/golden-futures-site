{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    <h1>{{university.university_name}}</h1>

    <h2>{{_("Courses")}}</h2>
    {% for category, courses in university.courses_by_category().items() %}
    <p>
        <i>{{ category.category_name }}</i>:
        {% for course in courses %}
            {{course.course_name}}
            {% if not loop.last %},{% endif %}
        {% endfor%}
    </p>
    {% endfor %}
    <h2>{{_("Admissions")}}</h2>
    <ul>
        {% for admission in university.admissions %}
        <li>{{ admission.admission_string }}</li>
        {% endfor %}
    </ul>
    
    <h2>{{_("Tuition Fees")}}</h2>
    <ul>
        {% for tuition_fee in university.tuition_fees %}
        <li>{{ tuition_fee }}</li>
        {% endfor %}
    </ul>

    <h2>{{_("Scholarships")}}</h2>
    <ul>
        {% for scholarship in university.scholarships %}
        <li>{{ scholarship.scholarship_string }}</li>
        {% endfor %}
    </ul>

    {% if university.facilities | length %}
    <h2>{{_("Facilities")}}</h2>
    <ul>
        {% for facility in university.facilities %}
        <li>{{ facility.facility_string }}</li>
        {% endfor %}
    </ul>
    {% endif %}

</div>

{% endblock %}