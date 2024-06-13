from db.sql_server import cursor as db_cursor
from utils.utils import build_fail_response_create, build_success_response_create


class InterfaceModelSQL:
    @staticmethod
    def get(criteria=None, params=None):
        if criteria:
            query = f"SELECT * FROM interfaces WHERE {criteria}"
        else:
            query = "SELECT * FROM interfaces"

        if params is not None:
            db_cursor.execute(query, params)
        else:
            db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description

        return result, column_description

    @staticmethod
    def getFilter(criteria=None, params=None):
        pass
    
    @staticmethod
    def get_ip_address_by_id_device(did):
        query = """
            SELECT TOP 1 ip_address 
                FROM interfaces 
                WHERE id_device = ?
                AND ip_address IS NOT NULL 
                AND ip_address <> '' 
                """
        db_cursor.execute(query, (did,))
        result = db_cursor.fetchone()
        if result:
            return result
        return None


    @staticmethod
    def create(data):
        query = """
        INSERT INTO interfaces (id_device, interface_name, ip_address, subnet_mask, cdp_state) 
        VALUES (?, ?, ?, ?, ?)
        """
        db_cursor.execute(
            query,
            (
                data["id_device"],
                data["interface_name"],
                data["ip_address"],
                data["mask"],
                data["cdp_state"],
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
        query = "UPDATE interfaces SET name = ?, price = ? WHERE id = ?"
        db_cursor.execute(query, (data["name"], data["price"], did))
        db_cursor.commit()
        return True  # Assuming successful update

    @staticmethod
    def delete_by_id(did):
        query = "DELETE FROM interfaces WHERE id = ?"
        db_cursor.execute(query, (did,))
        db_cursor.commit()
        return True  # Assuming successful deletion
