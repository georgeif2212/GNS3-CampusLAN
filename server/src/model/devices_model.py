from db.sql_server import cursor as db_cursor, conn as db_connection
from utils.utils import build_fail_response_create, build_success_response_create
from sqlalchemy.exc import IntegrityError, OperationalError


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
    def get_by_id(did):
        query = "SELECT * FROM devices WHERE id_device = ?"
        db_cursor.execute(query, (did,))
        result = db_cursor.fetchone()
        column_description = db_cursor.description
        if result:
            return result, column_description

        return None


    @staticmethod
    def get_by_hostname(hostname):
        query = "SELECT id_device FROM devices WHERE hostname = ?"
        db_cursor.execute(query, (hostname))
        result = db_cursor.fetchone()
        if result:
            return {"id_device": result[0]}
        return None


    @staticmethod
    def create(data):
        print(f"data: {data}")
        query = "INSERT INTO devices (hostname, software_version, model, serial_number) VALUES (?, ?, ?, ?)"
        try:
            db_cursor.execute(
                query,
                (
                    data["nombre_host"],
                    data["version_software"],
                    data["modelo"],
                    data["numero_serie"],
                ),
            )
            db_connection.commit()  # Asegúrate de usar db_connection.commit()

            # Obtener el número de filas afectadas
            rows_affected = db_cursor.rowcount

            if rows_affected > 0:
                print("Successful insertion")
                return build_success_response_create
            else:
                print("Failed insertion")
                return build_fail_response_create
        except IntegrityError as e:
            db_connection.rollback()  # Rollback en caso de error
            if "2627" in str(e):  # Código de error para clave duplicada
                return {"error": "Duplicate hostname", "status": 400}
            else:
                return {"error": str(e), "status": 500}
        except OperationalError as e:
            db_connection.rollback()  # Rollback en caso de error
            return {"error": str(e), "status": 500}
        except Exception as e:
            db_connection.rollback()  # Rollback en caso de error general
            return {"error": str(e), "status": 500}


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
