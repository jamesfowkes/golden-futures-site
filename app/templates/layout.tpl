<html lang="en">
<head>
    <meta charset="utf-8">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <link rel="stylesheet" href="{{url_for('static', filename='gf.css')}}">

    <title>Golden Futures University Guide 2017-2018</title>

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
              <a class="navbar-brand" href="#">Golden Futures University Guide 2017-2018</a>
            </div>
            <div id="nav" class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="{{url_for('website.render_index')}}">Home</a></li>
                    <li><a href="{{url_for('website.render_universities')}}">Universities</a></li>
                    <li><a href="{{url_for('website.render_courses')}}">Courses</a></li>
                </ul>
            </div>
        </nav>
    </div>
    </div>

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
{% endblock %}
<html>
