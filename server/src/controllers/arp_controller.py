from model.arp_model import ArpModelSQL
from model.devices_model import DeviceModelSQL
from utils.utils import (
    query_to_GNS3,
    default_query_ip,
    get_nested,
    build_success_response_create,
)
from flask import abort


class ArpController:
    @staticmethod
    def get(criteria=None):
        result, column_description = ArpModelSQL.get(criteria)
        # * Convert data into a dict
        data = []
        column_names = [column[0] for column in column_description]

        for record in result:
            data.append(dict(zip(column_names, record)))

        return data

    @staticmethod
    async def get_by_id(aId):
        pass

    @staticmethod
    def create(request, endpoint):
        ip_address = request.get("ip", default_query_ip)
        id_device = request.get("id_device")

        if not id_device:
            abort(400, description=" id_device is missing")

        gns3_data = query_to_GNS3(ip_address, endpoint)
        insert_interfaces(gns3_data, id_device)
        return build_success_response_create

    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass


def insert_interfaces(gns3_data, id_device):
    interfaces = (
        gns3_data.get("Cisco-IOS-XE-native:native", {})
        .get("interface", {})
        .get("GigabitEthernet", [])
    )

    for interface in interfaces:
        interface_name = f"GigabitEthernet{interface.get('name')}"
        ip_address = get_nested(interface, ["ip", "address", "primary", "address"], "")
        mask = get_nested(interface, ["ip", "address", "primary", "mask"], "")
        cdp_state = get_nested(interface, ["Cisco-IOS-XE-cdp:cdp", "enable"], False)

        data = {
            "id_device": id_device,
            "interface_name": interface_name,
            "ip_address": ip_address,
            "mask": mask,
            "cdp_state": cdp_state,
        }
        print(data)
        ArpModelSQL.create(data)

    return {}
