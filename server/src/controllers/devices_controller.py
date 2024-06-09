from model.devices_model import DeviceModelSQL
from utils.utils import query_to_GNS3


class DevicesController:
    @staticmethod
    def get(criteria=None):
        result, column_description = DeviceModelSQL.get(criteria)
        # * Convert data into a dict
        insertObject = []
        column_names = [column[0] for column in column_description]

        for record in result:
            insertObject.append(dict(zip(column_names, record)))

        return insertObject

    @staticmethod
    def get_by_id(dId):
        # Obtiene el resultado de la consulta
        result = DeviceModelSQL.get_by_id(dId)

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
        json_data = query_to_GNS3(ip, endpoint)
        data = {
            "nombre_host": json_data.get("Cisco-IOS-XE-native:native", {}).get("hostname", ""),
            "version_software": json_data.get("Cisco-IOS-XE-native:native", {}).get("version", ""),
            "modelo": json_data.get("Cisco-IOS-XE-native:native", {}).get("license", {}).get("udi", {}).get("pid", ""),
            "numero_serie": json_data.get("Cisco-IOS-XE-native:native", {}).get("license", {}).get("udi", {}).get("sn", "")
        }
        result = DeviceModelSQL.create(data)
        return result

    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass
