from flask import request, redirect, url_for, Response

from app.application import app

@app.route("/index", methods=['GET'])
def render_index():
    return Response(200)
