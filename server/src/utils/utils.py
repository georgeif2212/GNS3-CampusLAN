import requests
from dotenv import load_dotenv
import os

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
