<html lang="en">
<head>
    <meta charset="utf-8">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <link rel="stylesheet" href="{{url_for('static', filename='gf.css')}}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
    
    <title>{{_("Golden Futures University Guide 2017-2018")}}</title>

</head>

{% block body %}
<body>
    <div class="container">
        <nav class="navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <img class="navbar-brand" src="{{url_for('static', filename='golden-futures-logo.png')}}"/>
                    <a class="navbar-brand" href="#">{{_("Golden Futures University Guide 2017-2018")}}</a>
                </div>
                <div id="nav" class="navbar-collapse collapse">
                    <ul class="nav navbar-nav">
                        <li class={{"active" if g.active=="index" else ""}}>
                            <a href="{{url_for('website.render_index')}}">{{_("Home")}}</a>
                        </li>
                        <li class={{"active" if g.active=="universities" else ""}}>
                            <a href="{{url_for('website.render_universities')}}">{{_("Universities")}}</a>
                        </li>
                        <li class={{"active" if g.active=="categories" else ""}}>
                            <a href="{{url_for('website.render_courses')}}">{{_("Courses")}}</a>
                        </li>
                    </ul>
                    <ul class="nav navbar-nav navbar-right">
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
            </div>
        </nav>
    </div>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha256-k2WSCIexGzOj3Euiig+TlR8gA0EmPjuc79OEeY5L45g=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
{% endblock %}
<html>
