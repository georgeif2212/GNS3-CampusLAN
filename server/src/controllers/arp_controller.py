from model.arp_model import ArpModelSQL
from controllers.interfaces_controller import InterfacesController
import utils.utils as Utils
from utils.CustomError import CustomError
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
    def get_by_id_device(dId):
        result, column_description = ArpModelSQL.get_by_id_device(dId)
        if not result:
            raise CustomError(
                name="No ARP table Found",
                cause=f"No arp_table found for device ID {dId}",
                message=f"No arp_table found for device ID {dId}",
                code=404
            )
        return Utils.convert_data_into_dict(result,column_description)

    @staticmethod
    def create(request, endpoint):
        from controllers.devices_controller import DevicesController
        id_device = request.get("id_device")
        if not id_device:
            abort(400, description="missing UUID")

        if not Utils.is_valid_uuid(id_device):
            abort(400, description="invalid UUID Format")

        device = DevicesController.get_by_id(id_device)
        if not device:
            abort(400, description="device not found")

        ip_address_from_device = InterfacesController.get_ip_address_by_id_device(
            device["id_device"]
        )
        print(f"ipaddress: {ip_address_from_device}")

        gns3_data = Utils.query_to_GNS3(ip_address_from_device, endpoint)

        if gns3_data.get("status") == "Error executing curl command":
            abort(400, description=gns3_data.get("error", "Error connecting to GNS3"))

        print(gns3_data)

        insert_arp_entries(gns3_data, id_device)
        return Utils.build_success_response_create


    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass


def insert_arp_entries(gns3_data, id_device):
    arp_entries = gns3_data.get("Cisco-IOS-XE-arp-oper:arp-data", {}).get("arp-vrf", [])

    for vrf in arp_entries:
        for arp_oper in vrf.get("arp-oper", []):
            data = {
                "id_device": id_device,
                "ip_address": arp_oper.get("address", ""),
                "encryption_type": arp_oper.get("enctype", ""),
                "interface_name": arp_oper.get("interface", ""),
                "link_type": arp_oper.get("type", ""),
                "arp_mode": arp_oper.get("mode", ""),
                "hardware_type": arp_oper.get("hwtype", ""),
                "mac_address": arp_oper.get("hardware", ""),
            }

            # Print the data for debugging
            print("ARP Entry Data:", data)

            # Insert the data into the database
            ArpModelSQL.create(data)

    return {}
