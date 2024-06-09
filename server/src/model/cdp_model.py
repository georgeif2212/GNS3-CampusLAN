from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create


class CdpModelSQL:
    @staticmethod
    def get():
        query = "SELECT * FROM cdp_neighbors"
        db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description
        if result:
            return result, column_description

        return None

    @staticmethod
    def create(data):
        query = """INSERT INTO cdp_neighbors 
                    (id_device, ip_address, encryption_type, interface_name, link_type, cdp_mode, hardware_type, mac_address) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        db_cursor.execute(
            query,
            (
                data["id_device"],
                data["ip_address"],
                data["encryption_type"],
                data["interface_name"],
                data["link_type"],
                data["cdp_mode"],
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
        query = "UPDATE cdp_neighbors SET name = ?, price = ? WHERE id = ?"
        db_cursor.execute(query, (data["name"], data["price"], did))
        db_cursor.commit()
        return True  # Assuming successful update

    @staticmethod
    def delete_by_id(did):
        query = "DELETE FROM cdp_neighbors WHERE id = ?"
        db_cursor.execute(query, (did,))
        db_cursor.commit()
        return True  # Assuming successful deletion
