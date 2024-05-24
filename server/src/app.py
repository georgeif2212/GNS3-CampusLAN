from flask import Flask, request, jsonify
from db.sql_server import cursor as db_cursor
import requests
import os

from routers.api.devices_router import devices_router
from routers.api.interfaces_router import interfaces_router
from routers.api.queries_router import queries_router

from bfs import bfs_algorithm
from utils.utils import build_request_command
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Registrar los Blueprints en la aplicación
app.register_blueprint(devices_router, url_prefix="/api/devices")
app.register_blueprint(interfaces_router, url_prefix="/api/interfaces")
app.register_blueprint(queries_router, url_prefix="/api")


@app.route("/topology", methods=["GET"])
def topology():
    topology = bfs_algorithm()

    return jsonify(topology)


# Manejador de errores para excepciones específicas
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "status": e.code,
        "error": e.name,
        "message": e.description
    }).data
    response.content_type = "application/json"
    return response

# Manejador de errores para cualquier excepción no manejada
@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    response = jsonify({
        "status": code,
        "error": type(e).__name__,
        "message": str(e)
    })
    return response, code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)  # Abierto a conexiones externas


# sudo curl -k -u "admin:admin" -H "Accept: application/yang-data+json" https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-interfaces-ios-xe-oper:v4-protocol-stats/ --interface virbr0

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-route-map/ -k -u "admin:admin" -H "Accept: application/yang-data+json"


# sudo curl --interface virbr0 https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-module Cisco-IOS-XE-interfaces-oper { -k -u "admin:admin" -H "Accept: application/yang-data+json"


# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip/vrf-maximum-grouping:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-system-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json"
