from flask import Blueprint, jsonify, request
from controllers.devices_controller import DevicesController
import subprocess  # Para usar comandos como curl
import json
from utils.utils import (
    default_query_ip,
    build_curl_command,
)

queries_router = Blueprint("queries", __name__)

@queries_router.route("/arp", methods=["GET"])
def arp():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)

    # Usar la función para construir el comando `curl`
    command = build_curl_command(ip_address, "-arp-oper:arp-data/")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        arp_data = json.loads(result.stdout)
        bfs_result = {"message": "Data received", "arp": arp_data}
    else:
        bfs_result = {"message": "Error executing curl command"}

    return jsonify(bfs_result)


@queries_router.route("/native", methods=["GET"])
def native():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)

    command = build_curl_command(ip_address, "-native:native/")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        native_info = json.loads(result.stdout)
        bfs_result = {"message": "Data received", "native": native_info}
        return jsonify(bfs_result)
    else:
        bfs_result = {"message": "Error executing curl command"}
        return "Error executing curl command"


@queries_router.route("/cdp", methods=["GET"])
def cdp():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)

    command = build_curl_command(ip_address, "-cdp-oper:cdp-neighbor-details/")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        cdp_info = json.loads(result.stdout)
        bfs_result = {"message": "Data received", "cdp": cdp_info}
    else:
        bfs_result = {"message": "Error executing curl command"}

    return jsonify(bfs_result)


@queries_router.route("/lldp", methods=["GET"])
def lldp():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)

    command = build_curl_command(ip_address, "-lldp-oper:lldp-entries")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        lldp_info = json.loads(result.stdout)
        bfs_result = {"message": "Data received", "lldp": lldp_info}
    else:
        bfs_result = {"message": "Error executing curl command"}

    return jsonify(bfs_result)