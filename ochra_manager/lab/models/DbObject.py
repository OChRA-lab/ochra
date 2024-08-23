from ochra_common.base import DataModel
from ochra_common.connections.db_connection import DbConnection


class DbObject(DataModel):
    _collection: str = None

    def get_property(self, property_name):
        """Gets a property from the database using the db_data

        Args:
            property_name (str): property to get

        Returns:
            Any: property value
        """
        self.db_conn: DbConnection = DbConnection()
        return self.db_conn.read(self.db_data,
                                 property=property_name)

    @property
    def db_data(self):
        return {"id": self.id.hex, "_collection": self._collection}
