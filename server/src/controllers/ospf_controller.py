from model.ospf_model import OspfModelSQL
from controllers.devices_controller import DevicesController
from controllers.interfaces_controller import InterfacesController
import utils.utils as Utils
import utils.CustomError as CustomError
from flask import abort, jsonify


class OSPFController:
    @staticmethod
    def get():
        try:
            result, columns = OspfModelSQL.get()
            print(data)
            data = [Utils.rows_to_dict(row, columns) for row in result]
            return data
        except Exception as e:
            return jsonify({"error": str(e), "status": 500}), 500

    @staticmethod
    def get_ospf_by_id(ospf_id):
        try:
            result, columns = OspfModelSQL.get_ospf_by_id(ospf_id)
            if result:
                data = Utils.rows_to_dict(result, columns)
                return data
            else:
                abort(404, description="OSPF record not found")
        except Exception as e:
            return jsonify({"error": str(e), "status": 500}), 500

    @staticmethod
    def get_by_id_device(dId):
        result_ospf, column_description_ospf = OspfModelSQL.get_by_id_device(dId)
        if not result_ospf:
            raise CustomError(
                name="No ospf table Found",
                cause=f"No ospf table data found for device ID {dId}",
                message=f"No ospf table data found for device ID {dId}",
                code=404,
            )
        ospf = Utils.convert_data_into_dict(result_ospf, column_description_ospf)
        result_ospf_networks, column_description_ospf_networks = (
            OspfModelSQL.get_networks_by_id_device(dId)
        )
        if not result_ospf_networks:
            raise CustomError(
                name="No ospf networks Found",
                cause=f"No ospf networks found for device ID {dId}",
                message=f"No ospf networks found for device ID {dId}",
                code=404,
            )
        ospf_networks = Utils.convert_data_into_dict(
            result_ospf_networks, column_description_ospf_networks
        )
        return {"ospf_area": ospf, "ospf_networks": ospf_networks}

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

        return Utils.build_success_response_create

    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass


def insert_ospf_entries(gns3_data, device_id):
    ospf_data = (
        gns3_data.get("Cisco-IOS-XE-native:native", {})
        .get("router", {})
        .get("Cisco-IOS-XE-ospf:ospf", [])
    )

    if not ospf_data:
        print("No OSPF data found in the provided JSON.")
        return

    for ospf_entry in ospf_data:
        # Inserta las redes asociadas en la tabla ospf_networks
        ospf_process_id = ospf_entry.get("id")

        # Inserta el OSPF en la tabla ospf_table
        ospf_table_data = {
            "device_id": device_id,
            "ospf_process": int(ospf_process_id) + 1,
        }
        # Llama al modelo para insertar el OSPF principal
        OspfModelSQL.create_ospf_table_entry(ospf_table_data)

        networks = ospf_entry.get("network", [])

        for network in networks:
            print(network)
            ospf_network_data = {
                "id_device": device_id,
                "ospf_process_id": ospf_process_id,
                "network_ip_address": network.get("ip"),
                "mask": network.get("mask"),
                "area": network.get("area"),
            }

            # Llama al modelo para insertar las redes de OSPF

            OspfModelSQL.create_ospf_networks_entry(ospf_network_data)

    print("OSPF entries have been successfully inserted.")
