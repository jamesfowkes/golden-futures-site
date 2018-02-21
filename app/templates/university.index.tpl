{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    <h1><a class="link_no_underline" href="http://{{university.web_address}}">{{university.university_name}}</a></h1>

    <div class="card plain">
        <div class="card-title" role="tab" id="map_collapse_heading">
            <h3><a data-toggle="collapse" data-parent="#accordion" href="#map_collapse" aria-expanded="true" aria-controls="map_collapse">{{_("Show on Map")}}</a></h3>
        </div>
        <div id="map_collapse" class="collapse">
            <div id="map"></div>
        </div>
    </div>

    <div class="card plain">
        <h2>{{_("Contact Details")}}</h2>
        <ul>
        {% for detail in university.contact_details %}
            <li>{{ detail.contact_detail_string }}</li>
        {% endfor %}
        </ul>
    </div>

    <div class="card plain">
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
    </div>

    <div class="card plain">
        <h2>{{_("Admissions")}}</h2>
        <ul>
            {% for admission in university.admissions %}
            <li>{{ admission.admission_string }}</li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="card plain">
        <h2>{{_("Tuition Fees")}}</h2>
        <ul>
            {% for tuition_fee in university.tuition_fees %}
            <li>{{ tuition_fee }}</li>
            {% endfor %}
        </ul>
    </div>

    <div class="card plain">
        <h2>{{_("Scholarships")}}</h2>
        <ul>
            {% for scholarship in university.scholarships %}
            <li>{{ scholarship.scholarship_string }}</li>
            {% endfor %}
        </ul>
    </div>

    {% if university.facilities | length %}
    <div class="card plain">
        <h2>{{_("Facilities")}}</h2>
        <p>
        {{ university.facility_names() | join (", ") }}
        </p>
    </div>
    {% endif %}
    
    <link rel="stylesheet" href="{{url_for('static', filename='leaflet/leaflet.css')}}" />
    <script type="text/javascript" src="{{url_for('static', filename='leaflet/leaflet.js')}}"> </script>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="{{url_for('static', filename='leaflet/leafletembed.js')}}"></script>

</div>

{% endblock %}