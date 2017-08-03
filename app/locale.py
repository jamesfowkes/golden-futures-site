from flask import request, g

def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in app.config["SUPPORTED_LOCALES"]:
            g.current_lang = 'en'
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')
    else:
        g.current_lang = 'en'
    
def init_app(app):
    app.before_request(before)
