import logging

logger = logging.getLogger(__name__)

def get_request_languages(request):
    try:
        if request.method == 'POST':
            return request.form["languages"].split(",")
        else:
            return request.args["languages"].split(",")
    except:
        logger.error("Expected languages string in request")
        raise

def get_request_field(request, fieldname):
    try:
        if request.method == 'POST':
            return request.form[fieldname]
        else:
            return request.args[fieldname]
    except:
        logger.error("Fieldname %s not in request data", fieldname)
        raise

def get_request_field_with_language(request, fieldname, language):
    return get_request_field(request, "{}[{}]".format(fieldname, language))

def get_request_list_with_language(request, fieldname, language):
    return get_request_field(request, "{}[{}][]".format(fieldname, language))

def get_req_data_by_language(request, fields):
    languages = get_request_languages(request)
    data = {}

    for language in languages:
        data[language] = {field: get_request_field_with_language(request, field, language) for field in fields}

    return data

def get_req_list_by_language(request, fields, new_field_keys=None):

    new_field_keys = new_field_keys or fields

    languages = get_request_languages(request)
    data = {}

    for language in languages:
        data[language] = {key_name: get_request_list_with_language(request, field, language) for key_name, field in zip(new_field_keys,fields)}

    return data

def get_i18n_list(request, arrayname, translation_name):

    def full_array_name(arrayname, language):
        return arrayname + "[" + language + "][]"

    languages = get_request_languages(request)
    data = []

    data_lists = [request.form.getlist(full_array_name(arrayname, language)) for language in languages]

    for datapoints in zip(*data_lists):
        language_datapoint = {}
        for index, language in enumerate(languages):
            language_datapoint[language] = {translation_name: datapoints[index]}
        data.append(language_datapoint)

    return data

def zip_and_tag_request_data_lists(request, listnames_to_zip):
    zipped_data = []

    number_of_lists = len(listnames_to_zip)
    lists = [request.form.getlist(l) for l in listnames_to_zip]  
    lengths = [len(l) for l in lists]
    if len(set(lengths)) > 1:
        raise Exception("Lists must be of identical length (got {})".format(",".join([str(l) for l in lengths])))

    for data in zip(*lists):
        zipped_data.append({name: datapoint for name, datapoint in zip(listnames_to_zip, data)})

    return zipped_data
