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
    def get_by_id_device(dId):
        query = """SELECT 
                    id_cdp,
                    neighbor_device_name,
                    neighbor_id_device,
                    advertisement_version,
                    capability,
                    datetime,
                    duplex,
                    local_interface_name,
                    neighbor_interface_name,
                    neighbor_ip_address,
                    platform,
                    software_version
                FROM cdp_neighbors WHERE id_device = ?
                ORDER BY neighbor_device_name"""
        db_cursor.execute(query, (dId,))
        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description

    @staticmethod
    def create(data):
        query = """INSERT INTO cdp_neighbors 
                    (id_device, neighbor_id_device, neighbor_device_name, local_interface_name, neighbor_interface_name, 
                    capability, platform, software_version, duplex, advertisement_version, 
                    neighbor_ip_address) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        try:
            db_cursor.execute(
                query,
                (
                    data["id_device"],
                    data["neighbor_id_device"],
                    data["neighbor_device_name"],
                    data["local_interface_name"],
                    data["neighbor_interface_name"],
                    data["capability"],
                    data["platform"],
                    data["software_version"],
                    data["duplex"],
                    data["advertisement_version"],
                    data["neighbor_ip_address"],
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

        except Exception as e:
            print("Error inserting CDP data:", e)
            db_cursor.rollback()  # Rollback if there is an error
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
