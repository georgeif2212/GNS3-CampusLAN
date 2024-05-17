from collections import deque
from utils.utils import build_curl_command, default_query_ip, build_request_command
import subprocess  # Para usar comandos como curl
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


def get_interfaces_info(arp_data, pending_nodes, visited_nodes):
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

        if not interface or not ip_address or not mode:
            continue

        if interface not in temp_nodes:
            temp_nodes[interface] = {}

        if mode == "ios-arp-mode-interface":
            temp_nodes[interface]["local_ip"] = ip_address
        elif mode == "ios-arp-mode-dynamic":
            temp_nodes[interface].setdefault("neighbors", []).append(ip_address)

    for interface, data in temp_nodes.items():
        if "local_ip" in data and "neighbors" in data:
            local_ip = data["local_ip"]
            for neighbor_ip in data["neighbors"]:
                nodes[interface] = [local_ip, neighbor_ip]
                if all(
                    neighbor_ip not in iface[0]
                    for node in visited_nodes
                    for iface in node.values()
                ) and not neighbor_ip.startswith("192.168.122"):
                    pending_nodes.append(neighbor_ip)

    return nodes


def bfs_algorithm():
    queue_pending_nodes = deque()
    visited_nodes = []
    ip = "192.168.122.202"
    queue_pending_nodes.append(ip)
    i = 0

    while queue_pending_nodes:
        i += 1
        print(f"ITERACION: {i}, pending: {queue_pending_nodes}")

        current_ip = queue_pending_nodes.popleft()
        print(f"CURRENT IP: {current_ip}, {queue_pending_nodes}")
        arp_data = get_arp_data(current_ip)
        node = get_interfaces_info(arp_data, queue_pending_nodes, visited_nodes)

        if node:
            visited_nodes.append(node)

        if queue_pending_nodes:
            ip = queue_pending_nodes[0]
            print(f"COLA: {queue_pending_nodes}")

    print("Final visited nodes:", visited_nodes)
    return json.dumps(visited_nodes, indent=4)