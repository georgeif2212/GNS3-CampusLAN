from collections import deque
from utils.utils import build_curl_command, default_query_ip
import subprocess  # Para usar comandos como curl
import json


def bfs_algorithm():
    queue_to_be_visited = deque()
    command = build_curl_command(default_query_ip, "-arp-oper:arp-data/")

    result = subprocess.run(command, capture_output=True, text=True)
    arp_data = json.loads(result.stdout)

    # Añadimos direcciones a la cola (deque es serializable como lista)
    for arp_entry in arp_data["Cisco-IOS-XE-arp-oper:arp-data"]["arp-vrf"][0][
        "arp-oper"
    ]:
        if not arp_entry["address"].startswith("192.168.122."):
            queue_to_be_visited.append(arp_entry["address"])
    
    print("HOLA", queue_to_be_visited[0])

    command = build_curl_command(queue_to_be_visited[0], "-arp-oper:arp-data/")
    result = subprocess.run(command, capture_output=True, text=True)
    arp_data = json.loads(result.stdout)

    print(arp_data)

    return list(queue_to_be_visited)  # Convertir deque a lista para serializar
