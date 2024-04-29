from flask import Flask, request, jsonify
import subprocess  # Para usar comandos como curl
import json

app = Flask(__name__)

default_route="192.168.122.202"

@app.route('/arp', methods=['GET'])
def arp():
    data = request.get_json()
    ip_address = data.get("ip", default_route)
    
    # Aquí haces una consulta RESTCONF usando curl para obtener información del router
    command = [
        "sudo",
        "curl",
        "--interface", "virbr0",
        f"https://{ip_address}/restconf/data/Cisco-IOS-XE-arp-oper:arp-data/",
        "-k",  # Omitir verificación de certificados SSL
        "-u", "admin:admin",  # Usuario y contraseña
        "-H", "Accept: application/yang-data+json"
    ]
    
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
    ip_address = data.get("ip", default_route)
    
    # Aquí haces una consulta RESTCONF usando curl para obtener información del router
    command = [
        "sudo",
        "curl",
        "--interface", "virbr0",
        f"https://{ip_address}/restconf/data/Cisco-IOS-XE-native:native/",
        "-k",  # Ignorar verificación de certificados SSL
        "-u", "admin:admin",  # Usuario y contraseña
        "-H", "Accept: application/yang-data+json"
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        native_info = json.loads(result.stdout)
        bfs_result = {"message": "Data received", "native": native_info}
    else:
        bfs_result = {"message": "Error executing curl command"}

    return jsonify(bfs_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Abierto a conexiones externas




# sudo curl -k -u "admin:admin" -H "Accept: application/yang-data+json" https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-interfaces-ios-xe-oper:v4-protocol-stats/ --interface virbr0

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-route-map/ -k -u "admin:admin" -H "Accept: application/yang-data+json"


# sudo curl --interface virbr0 https://192.168.10.37:443/restconf/data/Cisco-IOS-XE-module Cisco-IOS-XE-interfaces-oper { -k -u "admin:admin" -H "Accept: application/yang-data+json" 


# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip/vrf-maximum-grouping:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-ip:maximum/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21:443/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-system-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json" -v

# sudo curl --interface virbr0 https://192.168.122.21/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/ -k -u "admin:admin" -H "Accept: application/yang-data+json"

