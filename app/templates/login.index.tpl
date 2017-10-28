{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    <h2>{{_("Administrator and Volunteer Login") }}</h2>

    {% with messages = get_flashed_messages() %}
    {% if messages %}
    {% for message in messages %}
    <div class="alert alert-warning">
    {{ message }}
    </div>
    {% endfor %}
    {% endif %}
    {% endwith %}

    <form id="login" method="POST" action="{{url_for('login_user')}}"">
        <div class="form-group">
            <label for="username" class="sr-only">{{_("Username")}}</label>
            <input class="form-control" type="text" name="username" placeholder="Username" required autofocus>
            <label for="password" class="sr-only">{{_("Password")}}</label>
            <input class="form-control" type="password" name="password" placeholder="Password" required>
            <button class="btn btn-default" type="submit">{{_("Login")}}</button>
        </div>
    </form>

</div>

{% endblock %}