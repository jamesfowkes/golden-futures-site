from flask import Blueprint

from flask import render_template

website = Blueprint('website', __name__, template_folder='templates')

@website.route("/index", methods=['GET'])
def render_index():
    return render_template('index.tpl')

@website.route("/universities", methods=['GET'])
def render_universities():
    return render_template('index.tpl')

@website.route("/courses", methods=['GET'])
def render_courses():
    return render_template('index.tpl')

def init_app(app):
    app.register_blueprint(website)
    