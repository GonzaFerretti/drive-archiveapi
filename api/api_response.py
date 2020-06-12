from flask import request, jsonify
from dicttoxml import dicttoxml
from api import app


def make_response(response):
    if request.accept_mimetypes.best == 'application/json':
        new_response = app.make_response(jsonify(response))
    else:
        new_response = app.make_response(dicttoxml(response, custom_root='response'))
        new_response.content_type = 'application/xml'

    return new_response