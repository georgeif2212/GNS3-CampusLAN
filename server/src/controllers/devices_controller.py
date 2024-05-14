from dao.devices_dao import DeviceDaoSQL


class DevicesController:
    @staticmethod
    def get(criteria=None):
        result, column_description = DeviceDaoSQL.get(criteria)
        # * Convert data into a dict
        insertObject = []
        column_names = [column[0] for column in column_description]

        for record in result:
            insertObject.append(dict(zip(column_names, record)))

        return insertObject

    @staticmethod
    async def get_by_id(dId):
        pass 

    @staticmethod
    def create(data):
        pass

    @staticmethod
    async def update_by_id(dId, data):
        pass

    @staticmethod
    async def delete_by_id(dId):
        pass
