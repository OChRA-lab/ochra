from ochra_common.utils.singleton_meta import SingletonMeta
from .mongo_adapter import MongoAdapter
import logging
from typing_extensions import Self


class DbConnection(metaclass=SingletonMeta):
    """database connection"""

    def __init__(
        self,
        hostname: str = "127.0.0.1:27017",
        db_name: str = "ochra_test_db",
        logger: logging.Logger = None,
    ) -> Self:
        """Constructor for DbConnection

        Args:
            hostname (str, optional): address of db host. Defaults to "127.0.0.1:27017"
            db_name (str, optional): name of the db. Defaults to "ochra_test_db"
            logger (logging.Logger, optional): logger if you have one.
                Defaults to None.
        """
        self.db_adapter: MongoAdapter = MongoAdapter(hostname, db_name, logger)

    def create(self, db_data, doc):
        """Create a new document in the specified collection."""
        return self.db_adapter.create(db_data, doc)

    def read(self, db_data, property=None, file=False, query=None):
        """Read documents from the specified collection that match the query."""

        return self.db_adapter.read(db_data, property, file=file, query=query)

    def update(self, db_data, update):
        """Update documents in the specified collection that match the query."""
        return self.db_adapter.update(db_data, update)

    def delete(self, db_data):
        """Delete documents from the specified collection that match the query."""
        return self.db_adapter.delete(db_data)

    def find(self, db_data, search_params: dict):
        """Find documents from the specified collection that match the query."""
        return self.db_adapter.find(db_data, search_params)
