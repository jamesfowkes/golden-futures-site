{% extends "layout.tpl" %}

{% block content %}
<div class="container">
    <h2>{{_("Administrator and Volunteer Login") }}</h2>
    <form id="login">
        <div class="form-group">
            <label for="username" class="sr-only">{{_("Username")}}</label>
            <input class="form-control" type="text" name="username" placeholder="Username" required autofocus>
            <label for="password" class="sr-only">{{_("Password")}}</label>
            <input class="form-control" type="password" name="password" placeholder="Password" required>
            <button class="btn" type="submit">{{_("Login")}}</button>
        </div>
    </form>

</div>

{% endblock %}