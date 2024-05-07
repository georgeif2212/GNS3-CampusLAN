from flask import Flask, request, jsonify
import subprocess  # Para usar comandos como curl
import json
import os
from bfs import bfs_algorithm

app = Flask(__name__)

default_query_ip="192.168.122.202"
query_base="/restconf/data/Cisco-IOS-XE"

# Función para generar el comando `curl`
def build_curl_command(ip_address, endpoint):
    command = [
        "sudo",
        "curl",
        "--interface", "virbr0",
        f"https://{ip_address}{query_base}{endpoint}",
        "-k",  # Ignorar verificación de certificados SSL
        "-u", "admin:admin",  # Usuario y contraseña
        "-H", "Accept: application/yang-data+json"
    ]
    return command

@app.route('/arp', methods=['GET'])
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

@app.route('/native', methods=['GET'])
def native():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)
    
    command = build_curl_command(ip_address, "-native:native/")

    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        native_info = json.loads(result.stdout)
        bfs_result = {"message": "Data received", "native": native_info}
    else:
        bfs_result = {"message": "Error executing curl command"}

    return jsonify(bfs_result)

# @app.route('/cdp', methods=['GET'])
# def cdp():
#     data = request.get_json() 
#     ip_address = data.get("ip", default_query_ip) 

    
#     result = subprocess.run(command, capture_output=True, text=True)
    
#     if result.returncode == 0:
#         cdp_info = json.loads(result.stdout)  # Convierte la salida a JSON

#         # Guarda el resultado en un archivo JSON
#         output_file_path = os.path.join(os.getcwd(), "cdp_results.json")  # Ruta del archivo JSON
#         with open(output_file_path, 'w') as file:
#             json.dump(cdp_info, file, indent=4)  # Guarda el JSON con una indentación legible
        
#         bfs_result = {"message": "Data received", "cdp": cdp_info}  # Respuesta para el cliente
#     else:
#         bfs_result = {"message": "Error executing curl command"}
    
#     # Devuelve la respuesta como JSON
#     return jsonify(bfs_result)

@app.route('/cdp', methods=['GET'])
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

@app.route('/topology', methods=['GET'])
def topology():
    return bfs_algorithm()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Abierto a conexiones externas




# sudo curl -k -u "admin:admin" -H "Accept: application/yang-data+json" https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-interfaces-ios-xe-oper:v4-protocol-stats/ --interface virbr0

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-route-map/ -k -u "admin:admin" -H "Accept: application/yang-data+json"


# sudo curl --interface virbr0 https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-module Cisco-IOS-XE-interfaces-oper { -k -u "admin:admin" -H "Accept: application/yang-data+json" 


# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip/vrf-maximum-grouping:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-system-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json"

