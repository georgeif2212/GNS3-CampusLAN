from collections import deque
from utils.utils import build_curl_command, default_query_ip, build_request_command
import subprocess
import json
import requests
from flask import jsonify


def get_arp_data(ip_address):
    arp_endpoint = "-arp-oper:arp-data/"
    command = build_curl_command(ip_address, arp_endpoint)
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        arp_data = json.loads(result.stdout)
        return arp_data
    except subprocess.CalledProcessError as e:
        print(f"Error during curl command execution: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def get_interfaces_info(ip, pending_ips, visited_nodes, visited_ips):
    # * if ip is already visited, don't query arp
    if ip in visited_ips:
        return None

    arp_data = get_arp_data(ip)
    nodes = {}

    if not arp_data:
        return nodes

    arp_entries = (
        arp_data.get("Cisco-IOS-XE-arp-oper:arp-data", {})
        .get("arp-vrf", [{}])[0]
        .get("arp-oper", [])
    )

    temp_nodes = {}
    for entry in arp_entries:
        interface = entry.get("interface")
        ip_address = entry.get("address")
        mode = entry.get("mode")

        if interface not in temp_nodes:
            temp_nodes[interface] = {}

        if mode == "ios-arp-mode-interface":
            temp_nodes[interface]["local_ip"] = ip_address
            # Añadir IP local a visited_ips
            visited_ips.add(ip_address)
        elif mode == "ios-arp-mode-dynamic":
            temp_nodes[interface].setdefault("neighbors", []).append(ip_address)

    for interface, data in temp_nodes.items():
        if "local_ip" in data and "neighbors" in data:
            local_ip = data["local_ip"]
            for neighbor_ip in data["neighbors"]:
                nodes[interface] = [local_ip, neighbor_ip]

                # Verificar si la IP vecina ya ha sido visitada
                if neighbor_ip not in visited_nodes and not neighbor_ip.startswith(
                    "192.168.122"
                ):
                    pending_ips.append(neighbor_ip)

    return nodes

def bfs_algorithm():
    queue_pending_ips = deque()
    visited_nodes = []
    visited_ips = set()
    ip = "192.168.122.202"
    queue_pending_ips.append(ip)


    while queue_pending_ips:
        # print(f"ITERACION: {i}, pending: {queue_pending_ips}")
        # print(f"VISITED_NODES: {visited_nodes}")
        # print(f"VISITED_IPS: {visited_ips}")
        current_ip = queue_pending_ips.popleft()
        # print(f"CURRENT IP: {current_ip}, {queue_pending_ips}")
        node = get_interfaces_info(
            current_ip, queue_pending_ips, visited_nodes, visited_ips
        )

        if node:
            visited_nodes.append(node)

    print("Final visited nodes:", visited_nodes)
    return json.dumps(visited_nodes, indent=2)
