from flask import Flask, request, jsonify
from db.sql_server import cursor as db_cursor
import subprocess  # Para usar comandos como curl
import json
import requests
import os

from routers.api.devices_router import devices_router
from bfs import bfs_algorithm
from utils.utils import (
    default_query_ip,
    build_curl_command,
    build_request_command
)  # Importar variables de utils

app = Flask(__name__)

# Registrar los Blueprints en la aplicación
app.register_blueprint(devices_router, url_prefix='/api')


@app.route('/consulta')
def consulta_emulacion():

    # Realizar la solicitud HTTP con autenticación y encabezados
    try:
        response = build_request_command(default_query_ip,"-native:native")
        # Si la solicitud fue exitosa, devolver los datos obtenidos
        if response.status_code == 200:
            return response.json()
        else:
            return 'Error al realizar la solicitud: {}'.format(response.status_code)
    except requests.RequestException as e:
        return 'Error de conexión: {}'.format(str(e))

@app.route("/datos", methods=["GET"])
def obtener_datos():
    # Utilizar el cursor para ejecutar una consulta SQL
    sql_query = "SELECT * FROM devices"
    db_cursor.execute(sql_query)

    # Obtener los resultados de la consulta
    resultados = db_cursor.fetchall()
    
    # Convertir los datos a un diccionario
    insertObject = []
    column_names = [column[0] for column in db_cursor.description]

    for record in resultados:
        insertObject.append(dict(zip(column_names, record)))
    db_cursor.close()

    print(insertObject)
    # Convertir los resultados en un formato JSON y devolverlos
    return jsonify(insertObject) 


@app.route("/arp", methods=["GET"])
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


@app.route("/native", methods=["GET"])
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


@app.route("/cdp", methods=["GET"])
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


@app.route("/lldp", methods=["GET"])
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


@app.route("/topology", methods=["GET"])
def topology():
    # Llamamos a bfs_algorithm() para obtener datos filtrados
    queue_to_be_visited = bfs_algorithm()

    # Asegurarse de que el retorno sea serializable
    return jsonify(queue_to_be_visited)  # Devolver la lista directamente


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)  # Abierto a conexiones externas


# sudo curl -k -u "admin:admin" -H "Accept: application/yang-data+json" https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-interfaces-ios-xe-oper:v4-protocol-stats/ --interface virbr0

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-route-map/ -k -u "admin:admin" -H "Accept: application/yang-data+json"


# sudo curl --interface virbr0 https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-module Cisco-IOS-XE-interfaces-oper { -k -u "admin:admin" -H "Accept: application/yang-data+json"


# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip/vrf-maximum-grouping:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-system-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json"
