def get_request_languages(request):
    if request.method == 'POST':
        return request.form["languages"].split(",")
    else:
        return request.args["languages"].split(",")

def get_request_field(request, fieldname):
    if request.method == 'POST':
        return request.form[fieldname]
    else:
        return request.args[fieldname]

def get_request_field_with_language(request, fieldname, language):
    return get_request_field(request, fieldname + "." + language)

def get_req_data_by_language(request, fields):
    languages = get_request_languages(request)
    data = {}

    for language in languages:
        data[language] = {field: get_request_field_with_language(request, field, language) for field in fields}

    return data
