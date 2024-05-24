from model.interfaces_model import InterfaceModelSQL
from model.devices_model import DeviceModelSQL
from utils.utils import (
    query_to_GNS3,
    default_query_ip,
    get_nested,
    build_success_response_create,
)
from flask import abort


class InterfacesController:
    @staticmethod
    def get(criteria=None):
        result, column_description = InterfaceModelSQL.get(criteria)
        # * Convert data into a dict
        data = []
        column_names = [column[0] for column in column_description]

        for record in result:
            data.append(dict(zip(column_names, record)))

        return data

    @staticmethod
    async def get_by_id(dId):
        pass

    @staticmethod
    def create(request, endpoint):
        ip_address = request.get("ip", default_query_ip)
        id_device = request.get("id_device")
        hostname = request.get("hostname")

        if not id_device and not hostname:
            abort(400, description="Either id_device or hostname are missing")

        gns3_data = query_to_GNS3(ip_address, endpoint)

        # If there is and id_devie, insert directly
        if id_device:
            insert_interfaces(gns3_data, id_device)
            return build_success_response_create

        # if the hostname came, first it has to get the id by the name
        if hostname:
            id_device = DeviceModelSQL.get_by_hostname(hostname)

            if not id_device:
                abort(404, description="Device with given hostname not found")
            insert_interfaces(gns3_data, id_device.get("id_device", {}))

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
        InterfaceModelSQL.create(data)

    return {}
