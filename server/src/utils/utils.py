import requests
from dotenv import load_dotenv
import os
import subprocess
import json
from flask import jsonify

load_dotenv()

default_query_ip = "192.168.122.202"
query_base = "/restconf/data/Cisco-IOS-XE"

# Datos de autenticación
username = os.getenv("USERNAME-GNS3-DEVICES")
password = os.getenv("PWD-GNS3-DEVICES")

# Encabezados de la solicitud
headers = {"Accept": "application/yang-data+json"}


def build_curl_command(ip_address, endpoint):
    command = [
        "sudo",
        "curl",
        "--interface",
        "virbr0",
        f"https://{ip_address}{query_base}{endpoint}",
        "-k",  # Ignorar verificación de certificados SSL
        "-u",
        f"{username}:{password}",  # Usuario y contraseña
        "-H",
        "Accept: application/yang-data+json",
    ]
    return command


def build_request_command(ip_address, endpoint):
    try:
        response = requests.get(
            f"https://{ip_address}{query_base}{endpoint}",
            headers=headers,
            auth=(username, password),
            verify=False,
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during request to {ip_address}: {e}")
        return None


import subprocess
import json
from flask import jsonify


def query_to_GNS3(ip_address):
    try:
        command = build_curl_command(ip_address, "-arp-oper:arp-data/")
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            arp_data = json.loads(result.stdout)
            bfs_result = {"message": "Data received", "arp": arp_data}
        else:
            bfs_result = {
                "message": "Error executing curl command",
                "error": result.stderr,
            }
        return jsonify(bfs_result)

    except subprocess.CalledProcessError as e:
        return jsonify({"message": "Subprocess error", "error": str(e)})
    except json.JSONDecodeError as e:
        return jsonify({"message": "JSON decode error", "error": str(e)})
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)})
