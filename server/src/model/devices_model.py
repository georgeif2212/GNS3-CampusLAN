from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create


class DeviceModelSQL:
    @staticmethod
    def get(criteria=None):
        query = "SELECT * FROM devices"
        if criteria:
            query += f" WHERE {criteria}"
        db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description

    @staticmethod
    def create(data):
        print(f"data: {data}")
        query = "INSERT INTO devices (hostname, software_version, model, serial_number) VALUES (?, ?, ?, ?)"
        db_cursor.execute(
            query,
            (
                data["nombre_host"],
                data["version_software"],
                data["modelo"],
                data["numero_serie"],
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
