import requests
from dotenv import load_dotenv
import os
import subprocess
import json
from flask import jsonify

import uuid


load_dotenv()

default_query_ip = "192.168.122.202"
query_base = "/restconf/data/Cisco-IOS-XE"
endpoint_native = "-native:native/"
endpoint_arp="-arp-oper:arp-data/"
endpoint_hardware="-device-hardware-oper:device-hardware-data/"
endpoint_cdp="-cdp-oper:cdp-neighbor-details/"

# Datos de autenticación
username = os.getenv("USERNAME-GNS3-DEVICES")
password = os.getenv("PWD-GNS3-DEVICES")

# Encabezados de la solicitud
headers = {"Accept": "application/yang-data+json"}

build_success_response_create = {
    "status": "success",
    "message": "The resource has been created succesfully",
}

build_fail_response_create = {
    "status": "failed",
    "message": "The resource hasn't been created",
}

build_success_response_update = {
    "status": "success",
    "message": "The resource has been updated successfully",
}

build_fail_response_update = {
    "status": "failed",
    "message": "The resource hasn't been updated",
}

build_success_response_delete = {
    "status": "success",
    "message": "The resource has been deleted successfully",
}

build_fail_response_delete = {
    "status": "failed",
    "message": "The resource hasn't been deleted",
}



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


def query_to_GNS3(ip_address, query):
    try:
        command = build_curl_command(ip_address, query)
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
        else:
            bfs_result = {
                "status": "Error executing curl command",
                "error": result.stderr,
            }
        return bfs_result

    except subprocess.CalledProcessError as e:
        return jsonify({"message": "Subprocess error", "error": str(e)})
    except json.JSONDecodeError as e:
        return jsonify({"message": "JSON decode error", "error": str(e)})
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)})


def get_nested(dictionary, keys, default=None):
    for key in keys:
        dictionary = dictionary.get(key, default)
        if dictionary is default:
            break
    return dictionary


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def rows_to_dict(result,columns):
    return dict(zip([column[0] for column in columns], result))

def convert_data_into_dict(result, column_description):
    column_names = [column[0] for column in column_description]

    if isinstance(result, list):
        # Si el resultado es una lista de registros
        insertObject = []
        for record in result:
            insertObject.append(dict(zip(column_names, record)))
        return insertObject
    else:
        # Si el resultado es un solo registro
        return dict(zip(column_names, result))