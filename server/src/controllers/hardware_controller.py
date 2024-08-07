from model.hardware_model import HardwareModelSQL
from controllers.devices_controller import DevicesController
from controllers.interfaces_controller import InterfacesController
import utils.utils as Utils
import utils.CustomError as CustomError
from flask import abort


class HardwareController:
    @staticmethod
    def get(criteria=None):
        result, column_description = HardwareModelSQL.get(criteria)
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
        result, column_description = HardwareModelSQL.get_by_id_device(dId)
        if not result:
            raise CustomError(
                name="No hardware table Found",
                cause=f"No hardware data found for device ID {dId}",
                message=f"No hardware data found for device ID {dId}",
                code=404
            )
        return Utils.convert_data_into_dict(result,column_description)

    @staticmethod
    def create(request, endpoint):
        id_device = request.get("id_device")
        if not id_device:
            abort(400, description="missing UUID")

        if not Utils.is_valid_uuid(id_device):
            abort(400, description="invalid UUID Format")

        device = DevicesController.get_by_id(id_device)
        print("device", device)
        if not device:
            abort(400, description="device not found")

        ip_address_from_device = InterfacesController.get_ip_address_by_id_device(
            device["id_device"]
        )
        print(f"ipaddress: {ip_address_from_device}")

        gns3_data = Utils.query_to_GNS3(ip_address_from_device, endpoint)

        if gns3_data.get("status") == "Error executing curl command":
            abort(400, description=gns3_data.get("error", "Error connecting to GNS3"))

        # print(gns3_data)
        

        insert_hardware_entries(gns3_data, id_device)
        return Utils.build_success_response_create


    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass


def insert_hardware_entries(gns3_data, id_device):
    device_inventory = gns3_data.get("Cisco-IOS-XE-device-hardware-oper:device-hardware-data", {}).get("device-hardware", {}).get("device-inventory",[])

    
    for device in device_inventory:
        data = {
            "id_device": id_device,
            "hw_type": device.get("hw-type", ""),
            "hw_dev_index": device.get("hw-dev-index", ""),
            "version": device.get("version", ""),
            "part_number": device.get("part-number", ""),
            "serial_number": device.get("serial-number", ""),
            "hw_description": device.get("hw-description", ""),
        }

        # Print the data for debugging
        # print("hardware Entry Data:", data)

        # Insert the data into the database
        HardwareModelSQL.create(data)

    return {}
