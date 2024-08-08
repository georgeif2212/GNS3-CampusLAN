from model.cdp_model import CdpModelSQL
from controllers.devices_controller import DevicesController
from controllers.interfaces_controller import InterfacesController
import utils.utils as Utils
from flask import abort
import utils.CustomError as CustomError


class CdpController:
    @staticmethod
    def get():
        result = CdpModelSQL.get()
        if result is None:
            return None
        
        record, column_description = result

        if record is not None:
        # * Convert data into a dict
            column_names = [column[0] for column in column_description]
            record_dict = dict(zip(column_names, record))
            return record_dict

        return None


    @staticmethod
    async def get_by_id(aId):
        pass

    @staticmethod
    def get_by_id_device(dId):
        result, column_description = CdpModelSQL.get_by_id_device(dId)
        if not result:
            raise CustomError(
                name="No CDP neighbors Found",
                cause=f"No cdp_table found for device ID {dId}",
                message=f"No cdp_table found for device ID {dId}",
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
        print(f"ip Address: {ip_address_from_device}")


        gns3_data = Utils.query_to_GNS3(ip_address_from_device, endpoint)

        if gns3_data.get("status") == "Error executing curl command":
            abort(400, description=gns3_data.get("error", "Error connecting to GNS3"))
    
        insert_cdp_entries(gns3_data, id_device)
        return Utils.build_success_response_create


    @staticmethod
    async def update_by_id(dId, data):
        pass


    @staticmethod
    async def delete_by_id(dId):
        pass


def insert_cdp_entries(gns3_data, id_device):
    cdp_neighbors = (
        gns3_data.get("Cisco-IOS-XE-cdp-oper:cdp-neighbor-details", {})
        .get("cdp-neighbor-detail", [])
    )

    for neighbor in cdp_neighbors:
        software_version_full = neighbor.get("version", "")
        # Solo almacenar hasta el primer salto de línea
        software_version = software_version_full.split("\n")[0] if software_version_full else ""

        # Obtener el ID del dispositivo vecino usando el nombre del dispositivo
        neighbor_device_name = neighbor.get("device-name", "")
        device_neighbor = DevicesController.get_device_by_hostname(neighbor_device_name)

        data = {
            "id_device": id_device,
            "neighbor_id_device": device_neighbor['id_device'],
            "neighbor_device_name": neighbor_device_name,
            "local_interface_name": neighbor.get("local-intf-name", ""),
            "neighbor_interface_name": neighbor.get("port-id", ""),
            "capability": neighbor.get("capability", "").strip(),
            "platform": neighbor.get("platform-name", ""),
            "software_version": software_version,
            "duplex": neighbor.get("duplex", ""),
            "advertisement_version": neighbor.get("adv-version", ""),
            "neighbor_ip_address": neighbor.get("ip-address", ""),
        }

        # Insert the data into the database
        CdpModelSQL.create(data)

    return {}

