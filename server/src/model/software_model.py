from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create


class SoftwareModelSQL:
    @staticmethod
    def get(criteria=None):
        query = "SELECT * FROM software"
        if criteria:
            query += f" WHERE {criteria}"
        db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description
    
    @staticmethod
    def get_by_id_device(dId):
        query = """SELECT 
                    id_software,
                    current_time_device,
                    boot_time,
                    software_version,
                    rommon_version,
                    last_reboot_reason
                FROM software WHERE id_device = ?"""
        db_cursor.execute(query, (dId,))
        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description

    @staticmethod
    def create(data):
        query = """INSERT INTO software 
                    (id_device, current_time_device, boot_time, software_version, rommon_version, last_reboot_reason) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
        db_cursor.execute(
            query,
            (
                data["id_device"],
                data["current_time_device"],
                data["boot_time"],
                data["software_version"],
                data["rommon_version"],
                data["last_reboot_reason"],
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
    def update_by_id(hid, data):
        query = "UPDATE software SET name = ?, price = ? WHERE id = ?"
        db_cursor.execute(query, (data["name"], data["price"], hid))
        db_cursor.commit()
        return True  # Assuming successful update

    @staticmethod
    def delete_by_id(hid):
        query = "DELETE FROM software WHERE id = ?"
        db_cursor.execute(query, (hid,))
        db_cursor.commit()
        return True  # Assuming successful deletion
