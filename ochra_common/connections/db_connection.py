from ochra_common.utils.singleton_meta import SingletonMeta
from ochra_common.connections.mongo_adapter import MongoAdapter
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

    def create(self, collection_name, document):
        """Create a new document in the specified collection."""
        return self.db_adapter.create(collection_name, document)

    def read(self, collection_name, object_id, property=None, file=False):
        """Read documents from the specified collection that match the query."""

        return self.db_adapter.read(collection_name,
                                    object_id, property, file=file)

    def update(self, collection_name, object_id, update):
        """Update documents in the specified collection that match the query."""
        return self.db_adapter.update(collection_name, object_id, update)

    def delete(self, collection_name, object_id):
        """Delete documents from the specified collection that match the query."""
        return self.db_adapter.delete(collection_name, object_id)
