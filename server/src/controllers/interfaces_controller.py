from model.interfaces_model import InterfaceModelSQL
from utils.utils import query_to_GNS3


class InterfacesController:
    @staticmethod
    async def get(criteria=None):
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
    async def create(ip, endpoint):
        pass

    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass
