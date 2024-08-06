from flask import Flask, jsonify

from routers.api.devices_router import devices_router
from routers.api.interfaces_router import interfaces_router
from routers.api.queries_router import queries_router
from routers.reports.reports_router import reports_router
from routers.api.arp_router import arp_router
from routers.api.cdp_router import cdp_router
from routers.api.ospf_router import ospf_router
from routers.api.hardware_router import hardware_router
from routers.api.software_router import software_router


from bfs import bfs_algorithm
from werkzeug.exceptions import HTTPException
from utils.utils import query_to_GNS3

app = Flask(__name__)

# Registrar los Blueprints en la aplicación
app.register_blueprint(reports_router, url_prefix="/reports")
app.register_blueprint(devices_router, url_prefix="/api/devices")
app.register_blueprint(interfaces_router, url_prefix="/api/interfaces")
app.register_blueprint(arp_router, url_prefix="/api/arp")
app.register_blueprint(hardware_router, url_prefix="/api/hardware")
app.register_blueprint(software_router, url_prefix="/api/software")
app.register_blueprint(cdp_router, url_prefix="/api/cdp")
app.register_blueprint(ospf_router, url_prefix="/api/ospf")
app.register_blueprint(queries_router, url_prefix="/api")


@app.route("/topology", methods=["GET"])
def topology():
    topology = bfs_algorithm()

    return jsonify(topology)

@app.route("/test", methods=["GET"])
def test():
    gns3_data= query_to_GNS3("192.168.10.14", "-native:native/")

    return jsonify(gns3_data)


# Manejador de errores para excepciones específicas
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify(
        {"status": e.code, "error": e.name, "message": e.description}
    ).data
    response.content_type = "application/json"
    return response


# Manejador de errores para cualquier excepción no manejada
@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    response = jsonify({"status": code, "error": type(e).__name__, "message": str(e)})
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
