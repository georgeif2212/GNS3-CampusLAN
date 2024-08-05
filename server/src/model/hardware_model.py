from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create


class HardwareModelSQL:
    @staticmethod
    def get(criteria=None):
        query = "SELECT * FROM hardware"
        if criteria:
            query += f" WHERE {criteria}"
        db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description

    @staticmethod
    def create(data):
        query = """INSERT INTO hardware 
                    (id_device, hw_type, hw_dev_index, version, part_number, serial_number, hw_description) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)"""
        db_cursor.execute(
            query,
            (
                data["id_device"],
                data["hw_type"],
                data["hw_dev_index"],
                data["version"],
                data["part_number"],
                data["serial_number"],
                data["hw_description"],
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
        query = "UPDATE hardware SET name = ?, price = ? WHERE id = ?"
        db_cursor.execute(query, (data["name"], data["price"], hid))
        db_cursor.commit()
        return True  # Assuming successful update

    @staticmethod
    def delete_by_id(hid):
        query = "DELETE FROM hardware WHERE id = ?"
        db_cursor.execute(query, (hid,))
        db_cursor.commit()
        return True  # Assuming successful deletion
