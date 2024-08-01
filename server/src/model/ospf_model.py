from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create, build_success_response_delete

from db.sql_server import cursor as db_cursor, conn as db_connection
from sqlalchemy.exc import IntegrityError, OperationalError

class OspfModelSQL:
    @staticmethod
    def get():
        query = "SELECT * FROM ospf_table"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        column_description = db_cursor.description
        if result:
            return result, column_description
        return None

    @staticmethod
    def get_ospf_by_id(ospf_id):
        query = "SELECT * FROM ospf_table WHERE ospf_id = ?"
        db_cursor.execute(query, (ospf_id,))
        result = db_cursor.fetchone()
        column_description = db_cursor.description
        if result:
            return result, column_description
        return None

    @staticmethod
    def get_networks_by_ospf_process_id(ospf_process_id):
        query = "SELECT * FROM ospf_networks WHERE ospf_process_id = ?"
        db_cursor.execute(query, (ospf_process_id,))
        result = db_cursor.fetchall()
        column_description = db_cursor.description
        if result:
            return result, column_description
        return None

    @staticmethod
    def create_ospf_networks_entry(data):
        try:
            # Insertar en ospf_networks
            query_networks = """
                INSERT INTO ospf_networks (ospf_process_id, id_device, network_ip_address, mask, area)
                VALUES (?, ?, ?, ?, ?)
            """
            db_cursor.execute(
                query_networks,
                (
                    data["ospf_process_id"],
                    data["id_device"],
                    data["network_ip_address"],
                    data["mask"],
                    data["area"]
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

        except IntegrityError as e:
            db_connection.rollback()
            if "2627" in str(e):
                return {"error": "Duplicate OSPF process ID", "status": 400}
            else:
                return {"error": str(e), "status": 500}

        except OperationalError as e:
            db_connection.rollback()
            return {"error": str(e), "status": 500}

        except Exception as e:
            db_connection.rollback()
            return {"error": str(e), "status": 500}

    @staticmethod
    def create_ospf_table_entry(ospf_table_data):
        query = "INSERT INTO ospf_table (device_id, ospf_process_id) VALUES (?, ?)"
        try:
            db_cursor.execute(
                query,
                (
                    ospf_table_data["device_id"],
                    ospf_table_data["ospf_process_id"],
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
    def update_ospf_by_id(ospf_id, data):
        try:
            # Iniciar transacción
            db_connection.begin()

            # Actualizar en ospf_table
            query_ospf = """
                UPDATE ospf_table 
                SET device_id = ?, ospf_process_id = ?
                WHERE ospf_id = ?
            """
            db_cursor.execute(
                query_ospf,
                (
                    data["device_id"],
                    data["ospf_process_id"],
                    ospf_id
                ),
            )

            # Borrar las redes antiguas y luego insertar las nuevas en ospf_networks
            query_delete_networks = """
                DELETE FROM ospf_networks WHERE ospf_process_id = ?
            """
            db_cursor.execute(query_delete_networks, (data["ospf_process_id"],))

            query_insert_networks = """
                INSERT INTO ospf_networks (ospf_process_id, network_ip_address, mask, area)
                VALUES (?, ?, ?, ?)
            """
            for network in data["networks"]:
                db_cursor.execute(
                    query_insert_networks,
                    (
                        data["ospf_process_id"],
                        network["network_ip_address"],
                        network["mask"],
                        network["area"]
                    ),
                )

            # Commit transacción si todo sale bien
            db_cursor.commit()

            return {"message": "OSPF data updated successfully"}, 200

        except IntegrityError as e:
            db_connection.rollback()
            if "2627" in str(e):
                return {"error": "Duplicate OSPF process ID", "status": 400}
            else:
                return {"error": str(e), "status": 500}

        except OperationalError as e:
            db_connection.rollback()
            return {"error": str(e), "status": 500}

        except Exception as e:
            db_connection.rollback()
            return {"error": str(e), "status": 500}

    @staticmethod
    def delete_ospf_by_id(ospf_id):
        try:

            db_connection.begin()

            # Obtener ospf_process_id antes de borrar
            query_get_process_id = "SELECT ospf_process_id FROM ospf_table WHERE ospf_id = ?"
            db_cursor.execute(query_get_process_id, (ospf_id,))
            ospf_process_id = db_cursor.fetchone()[0]

            # Borrar en ospf_networks
            query_delete_networks = "DELETE FROM ospf_networks WHERE ospf_process_id = ?"
            db_cursor.execute(query_delete_networks, (ospf_process_id,))

            # Borrar en ospf_table
            query_delete_ospf = "DELETE FROM ospf_table WHERE ospf_id = ?"
            db_cursor.execute(query_delete_ospf, (ospf_id,))

            # Commit transacción si todo sale bien
            db_connection.commit()

            return build_success_response_delete

        except OperationalError as e:
            db_connection.rollback()
            return {"error": str(e), "status": 500}

        except Exception as e:
            db_connection.rollback()
            return {"error": str(e), "status": 500}
