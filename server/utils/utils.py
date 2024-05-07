default_query_ip="192.168.122.202"
query_base="/restconf/data/Cisco-IOS-XE"

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