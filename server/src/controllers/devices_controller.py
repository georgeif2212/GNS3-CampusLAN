from model.devices_model import DeviceModelSQL
import utils.utils as Utils
from utils.CustomError import CustomError
from controllers.interfaces_controller import InterfacesController

import utils.utils as Utils


class DevicesController:
    @staticmethod
    def get(criteria=None):
        result, column_description = DeviceModelSQL.get(criteria)
        return Utils.convert_data_into_dict(result, column_description)

    @staticmethod
    def get_by_id(dId):
        if not dId:
            raise CustomError(
                name="No id_device",
                cause=f"No id_device was consulted {dId}",
                message=f"No id_device was consulted {dId}",
                code=404,
            )

        if not Utils.is_valid_uuid(dId):
            raise CustomError(
                name="Invalid id_device",
                cause=f"The id_device is wrong {dId}",
                message=f"The id_device is wrong {dId}",
                code=404,
            )

        # Obtiene el resultado de la consulta
        result = DeviceModelSQL.get_by_id(dId)

        # Verifica si el resultado es None
        if result is None:
            raise CustomError(
                name="Device not found",
                cause=f"Device ID {dId} does not exist",
                message=f"Device with ID {dId} not found",
                code=404,
            )

        device, column_description = result
        return Utils.convert_data_into_dict(device, column_description)

    @staticmethod
    def get_device_by_hostname(hostname):
        # Obtiene el resultado de la consulta
        result = DeviceModelSQL.get_device_by_hostname(hostname)

        # Verifica si el resultado es None
        if result is None:
            return None

        device, column_description = result

        if device is not None:
            # Convierte la fila del dispositivo en un diccionario
            column_names = [column[0] for column in column_description]
            record_dict = dict(zip(column_names, device))
            return record_dict

        return None

    @staticmethod
    def create(ip, endpoint):
        json_data = Utils.query_to_GNS3(ip, endpoint)
        data = {
            "nombre_host": json_data.get("Cisco-IOS-XE-native:native", {}).get(
                "hostname", ""
            ),
            "version_software": json_data.get("Cisco-IOS-XE-native:native", {}).get(
                "version", ""
            ),
            "modelo": json_data.get("Cisco-IOS-XE-native:native", {})
            .get("license", {})
            .get("udi", {})
            .get("pid", ""),
            "numero_serie": json_data.get("Cisco-IOS-XE-native:native", {})
            .get("license", {})
            .get("udi", {})
            .get("sn", ""),
        }
        result = DeviceModelSQL.create(data)
        return result

    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass

    @staticmethod
    def create_report_device(dId):
        from controllers.arp_controller import ArpController
        from controllers.cdp_controller import CdpController
        from controllers.software_controller import SoftwareController
        from controllers.hardware_controller import HardwareController
        from controllers.ospf_controller import OSPFController

        # Obtiene el resultado de la consulta
        device = DevicesController.get_by_id(dId)
        interfaces = InterfacesController.get_by_id_device(dId)
        arp_table = ArpController.get_by_id_device(dId)
        cdp_neighbors = CdpController.get_by_id_device(dId)
        software_device = SoftwareController.get_by_id_device(dId)
        hardware_device = HardwareController.get_by_id_device(dId)
        ospf_table = OSPFController.get_by_id_device(dId)
        data = {
            "device": {
                "general": {
                    "device_information": device,
                    "software": software_device,
                    "hardware": hardware_device,
                },
                "interfaces": interfaces,
                "arp_table": arp_table,
                "cdp_neighbors": cdp_neighbors,
                "ospf": ospf_table,
            },
        }
        return data
