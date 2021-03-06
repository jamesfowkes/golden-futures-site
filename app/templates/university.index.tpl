{% extends "layout.tpl" %}

{% import 'dashboard.macro' as dashboard_macro with context%}

{% block content %}
<div class="container">
    <div class="row align-items-end">
        <div class="col-sm">
            <h1>
                <a class="link_no_underline" href="http://{{university.web_address}}">{{university.university_name}}</a>
            </h1>
        </div>
        {% if current_user.is_authenticated and not university.is_pending() %}
        <div class="col-sm">
            
                <div class="float-right">
                    <a href="{{url_for('dashboard.render_edit_university_dashboard', university_id=university.university_id)}}">{{_("Edit this university")}}</a>
                </div>
        </div>
        {% endif %}
    </div>

    <div class="card plain">
        <h2>{{_("Quotes")}}</h2>
        <p>
        {% for quote in university.quotes %}
            <span class="quote"><q>{{ quote.quote_string }}</q></span>
        {% endfor %}
        <p>
    </div>

    <h2 class="print-only">{{university.web_address}}</h2>

    {% if g.ep_data["osm_url"] is not none %}    
    <div class="card plain">
        <div class="card-title" role="tab" id="map_collapse_heading">
            <h3><a data-toggle="collapse" data-parent="#accordion" href="#map_collapse" aria-expanded="true" aria-controls="map_collapse">{{_("Show on Map")}}</a></h3>
        </div>
        <div id="map_collapse" class="collapse">
            <div id="map"></div>
            <a href="#" id="open_map_link">{{_("Open map in new window")}}</a>
        </div>
    </div>
    {% endif %}

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
    
    {% if university.is_pending() %}
    <div class="row padded-top padded-bottom">
        <div class="col-sm">
            {{dashboard_macro.approve("university", university.pending_id, "btn-block")}}
        </div>
        <div class="col-sm">
             {{dashboard_macro.reject("university", university.pending_id, "btn-block")}}
        </div>
    </div>
    {% endif %}

</div>

{% endblock %}