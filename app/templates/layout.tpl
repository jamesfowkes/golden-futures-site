{% import 'navbar.macro' as navbar_macro with context%}

<html lang="en">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">

    <link rel="stylesheet" href="{{url_for('static', filename='gf.css')}}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
    
    <title>{{_("Golden Futures University Guide 2017-2018")}}</title>

    <script src="https://use.fontawesome.com/0bde7bffdf.js"></script>
    
    <script type=text/javascript>
        $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
        $L = {{ g.translations|tojson|safe }};
        $pagelang = "{{ g.lang }}";
        $data = {
            {% for k, v in g.ep_data.items() %}
            '{{k}}': '{{v}}',
            {% endfor %}
        };

    </script>
</head>

{% block body %}
<body>
    <div class="container">
        <nav class="navbar navbar-expand-lg navbar-light">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="sr-only">Toggle navigation</span>
                <span class="navbar-toggler-icon"></span>
            </button>
            <img class="navbar-brand" src="{{url_for('static', filename='golden-futures-logo.png')}}"/>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <span class="nav-item">{{_("Golden Futures University Guide 2017-2018")}}</span>
                <ul class="navbar-nav mr-auto">
                    {{ navbar_macro.li_navitem(g.active, "index") }}
                    {{ navbar_macro.a_navlink(g.active, "index", url_for('website.render_index'), "Home") }}
                    </li>
                    {{ navbar_macro.li_navitem(g.active, "universities") }}
                    {{ navbar_macro.a_navlink(g.active, "universities", url_for('website.render_universities'), "Universities") }}
                    </li>
                    {{ navbar_macro.li_navitem(g.active, "categories") }}
                    {{ navbar_macro.a_navlink(g.active, "categories", url_for('website.render_courses'), "Courses") }}
                    </li>

                {% if current_user.is_authenticated %}

                    </li>
                </ul>
                    {{ navbar_macro.render_user_menu() }}

                {% else %}
                    
                    {{ navbar_macro.li_navitem(g.active, "login") }}
                    {{ navbar_macro.a_navlink(g.active, "login", url_for('website.render_login'), "Login") }}
                    </li>
                </ul>
                    
                {% endif %}

                <ul class="nav navbar-nav ml-auto">
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">
                            {{ g.lang | language_name }}<span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" role="menu">
                            <li><a href="{{url_for(request.url_rule.endpoint, lang='km', **g.ep_data)}}" class="language">{{_("Khmer")}}</a></li>
                            <li><a href="{{url_for(request.url_rule.endpoint, lang='en', **g.ep_data)}}" class="language">{{_("English")}}</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </nav>
    </div>

    <div id="content" class="container">
        {% block content %}{% endblock %}
    </div>

    {% block js  %}
        <script src="{{url_for('static', filename='util.js')}}"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
        <script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
    {% endblock %}

</body>
{% endblock %}
<html>
