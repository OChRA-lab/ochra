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
    ) -> Self:
        """Constructor for DbConnection

        Args:
            hostname (str, optional): address of db host. Defaults to "127.0.0.1:27017"
            db_name (str, optional): name of the db. Defaults to "ochra_test_db"
        """
        self._logger = logging.getLogger(__name__)
        self.db_adapter: MongoAdapter = MongoAdapter(hostname, db_name, self._logger)
        

    def create(self, db_data, doc):
        """Create a new document in the specified collection."""
        self._logger.debug(f"Creating a document in collection: {db_data['_collection']}")
        return self.db_adapter.create(db_data, doc)

    def read(self, db_data, property=None, file=False):
        """Read documents from the specified collection that match the query."""
        self._logger.debug(f"Reading documents from collection: {db_data['_collection']}")
        return self.db_adapter.read(db_data, property, file=file)

    def update(self, db_data, update, file=False):
        """Update documents in the specified collection that match the query."""
        self._logger.debug(f"Updating documents in collection: {db_data['_collection']}")
        return self.db_adapter.update(db_data, update, file=file)

    def delete(self, db_data):
        """Delete documents from the specified collection that match the query."""
        self._logger.debug(f"Deleting documents from collection: {db_data['_collection']}")
        return self.db_adapter.delete(db_data)

    def find(self, db_data, search_params: dict):
        """Find a document from the specified collection that match the query."""
        self._logger.debug(f"Finding documents in collection: {db_data['_collection']}")
        return self.db_adapter.find(db_data, search_params)

    def find_all(self, db_data, search_params: dict):
        """Find all documents from the specified collection that match the query."""
        self._logger.debug(f"Finding all documents in collection: {db_data['_collection']}")
        return self.db_adapter.find_all(db_data, search_params)
