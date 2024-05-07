from collections import deque
from utils.utils import build_curl_command, default_query_ip
import subprocess  # Para usar comandos como curl

def bfs_algorithm():
    # queue = deque()

    command = build_curl_command(default_query_ip, "-arp-oper:arp-data/")

    result = subprocess.run(command, capture_output=True, text=True)
    print(result)
    return result