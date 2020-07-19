from flask import jsonify, redirect, request
from api import app
from api.api_response import make_response
import json
from api import operations_archive

@app.route("/api/archive/addfile/<client_label>/<file_name>", methods=["POST"])
def add_file(client_label,file_name):
    fileb64 = request.data.decode('utf-8')
    result = operations_archive.archive_file(fileb64, file_name, client_label)
    return result

# @app.route("/api/archive/setupclient/<client_label>/<client_name>", methods=["POST"])
# def setup_client(client_label,client_name):
#     result = operations_archive.setup_client(client_name,client_label)
#     return result

@app.route("/api/archive/updateclients", methods=["POST"])
def update_clients():
    result = operations_archive.update_clients_list()
    return result
       