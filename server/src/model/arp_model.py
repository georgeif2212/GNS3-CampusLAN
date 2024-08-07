from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create


class ArpModelSQL:
    @staticmethod
    def get(criteria=None):
        query = "SELECT * FROM arp"
        if criteria:
            query += f" WHERE {criteria}"
        db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description
    
    @staticmethod
    def get_by_id_device(dId):
        query = """SELECT arp_mode,
                        datetime,
                        encryption_type,
                        hardware_type,
                        id_arp,
                        interface_name,
                        ip_address,
                        link_type
                        mac_address
                    FROM arp WHERE id_device = ?"""
        db_cursor.execute(query, (dId,))
        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description

    @staticmethod
    def create(data):
        print(f"data: {data}")
        query = """INSERT INTO arp 
                    (id_device, ip_address, encryption_type, interface_name, link_type, arp_mode, hardware_type, mac_address) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        db_cursor.execute(
            query,
            (
                data["id_device"],
                data["ip_address"],
                data["encryption_type"],
                data["interface_name"],
                data["link_type"],
                data["arp_mode"],
                data["hardware_type"],
                data["mac_address"],
            ),
        )
        db_cursor.commit()

        # Obtain the number of affected rows
        rows_affected = db_cursor.rowcount

        if rows_affected > 0:
            print("Successful insertion")
            return build_success_response_create
        else:
            print("Failed insertion")
            return build_fail_response_create

    @staticmethod
    def update_by_id(did, data):
        query = "UPDATE devices SET name = ?, price = ? WHERE id = ?"
        db_cursor.execute(query, (data["name"], data["price"], did))
        db_cursor.commit()
        return True  # Assuming successful update

    @staticmethod
    def delete_by_id(did):
        query = "DELETE FROM devices WHERE id = ?"
        db_cursor.execute(query, (did,))
        db_cursor.commit()
        return True  # Assuming successful deletion
