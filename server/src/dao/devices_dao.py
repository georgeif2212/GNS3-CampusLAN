from db.sql_server import cursor as db_cursor


class DeviceDaoSQL:
    @staticmethod
    def get(criteria=None):
        query = "SELECT * FROM devices"
        if criteria:
            query += f" WHERE {criteria}"
        db_cursor.execute(query)

        result = db_cursor.fetchall()
        column_description = db_cursor.description

        db_cursor.close()
        return result, column_description

    @staticmethod
    def create(data):
        query = "INSERT INTO devices (NombreHost, VersionSoftware, Modelo, NumeroSerie) VALUES (?, ?)"
        db_cursor.execute(query, (data["name"], data["price"]))
        db_cursor.commit()
        db_cursor.close()
        return True  # Assuming successful creation

    @staticmethod
    def update_by_id(did, data):
        query = "UPDATE devices SET name = ?, price = ? WHERE id = ?"
        db_cursor.execute(query, (data["name"], data["price"], did))
        db_cursor.commit()
        db_cursor.close()
        return True  # Assuming successful update

    @staticmethod
    def delete_by_id(did):
        query = "DELETE FROM devices WHERE id = ?"
        db_cursor.execute(query, (did,))
        db_cursor.commit()
        db_cursor.close()
        return True  # Assuming successful deletion
