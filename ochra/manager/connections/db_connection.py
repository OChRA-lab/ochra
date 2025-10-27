from ochra.common.utils.singleton_meta import SingletonMeta
from .mongo_adapter import MongoAdapter
import logging
from typing_extensions import Self, Dict, Any


class DbConnection(metaclass=SingletonMeta):
    """
    DbConnection is a singleton class that provides an interface for interacting with any database.
    This class currently acts as a wrapper around the MongoAdapter, offering CRUD operations and query methods for managing documents
    within specified collections. However, any database adapter that adheres to the expected interface can be integrated in the future.
    
    Attributes:
        db_adapter (MongoAdapter): Adapter for MongoDB operations. This can be replaced with any other database adapter that follows the same interface.
    """

    def __init__(
        self,
        hostname: str = "127.0.0.1:27017",
        db_name: str = "ochra_test_db",
    ) -> Self:
        """
        Initialize a DbConnection instance.

        Args:
            hostname (str, optional): Address of the database host. Defaults to "127.0.0.1:27017".
            db_name (str, optional): Name of the database. Defaults to "ochra_test_db".
        """
        self._logger = logging.getLogger(__name__)
        self.db_adapter: MongoAdapter = MongoAdapter(hostname, db_name, self._logger)
        

    def create(self, db_data: Dict[str, Any], doc: Dict[str, Any]) -> Any:
        """
        Create a new document in the specified collection.

        Args:
            db_data (Dict[str, Any]): Dictionary containing database information, including the target collection.
            doc (Dict[str, Any]): The document to be created.

        Returns:
            Any: The result of the create operation, typically the created document or its identifier.
        """
        self._logger.debug(f"Creating a document in collection: {db_data['_collection']}")
        return self.db_adapter.create(db_data, doc)

    def read(self, db_data: Dict[str, Any], property: str = None, file: bool = False) -> Any:
        """
        Read documents from the specified collection that match the query.

        Args:
            db_data (Dict[str, Any]): Dictionary containing database information, including the target collection and query parameters.
            property (str, optional): Specific property to retrieve from the documents. Defaults to None.
            file (bool, optional): Flag indicating if the read operation involves file data. Defaults to False.

        Returns:
            Any: The result of the read operation, which could be a document, a specific property, or file data.
        """
        self._logger.debug(f"Reading documents from collection: {db_data['_collection']}")
        return self.db_adapter.read(db_data, property, file=file)

    def update(self, db_data: Dict[str, Any], update: Dict[str, Any], file: bool = False) -> Any:
        """
        Update documents in the specified collection that match the query.
        
        Args:
            db_data (Dict[str, Any]): Dictionary containing database information, including the target collection and query parameters.
            update (Dict[str, Any]): The update operations to be applied to the matching documents.
            file (bool, optional): Flag indicating if the update operation involves file data. Defaults to False.

        Returns:
            Any: The result of the update operation, typically the updated document or a status indicator.
        """
        self._logger.debug(f"Updating documents in collection: {db_data['_collection']}")
        return self.db_adapter.update(db_data, update, file=file)

    def delete(self, db_data: Dict[str, Any]) -> Any:
        """
        Delete documents from the specified collection that match the query.

        Args:
            db_data (Dict[str, Any]): Dictionary containing database information, including the target collection and query parameters.

        Returns:
            Any: The result of the delete operation, typically a status indicator or the count of deleted documents.
        """
        self._logger.debug(f"Deleting documents from collection: {db_data['_collection']}")
        return self.db_adapter.delete(db_data)

    def find(self, db_data: Dict[str, Any], search_params: Dict[str, Any]) -> Any:
        """
        Find documents from the specified collection that match the search parameters.

        Args:
            db_data (Dict[str, Any]): Dictionary containing database information, including the target collection.
            search_params (Dict[str, Any]): The search parameters to filter the documents.

        Returns:
            Any: The result of the find operation, typically a matching document or None if not found.
        """
        self._logger.debug(f"Finding documents in collection: {db_data['_collection']}")
        return self.db_adapter.find(db_data, search_params)

    def find_all(self, db_data: Dict[str, Any], search_params: Dict[str, Any]) -> Any:
        """
        Find all documents from the specified collection that match the query.

        Args:
            db_data (Dict[str, Any]): Dictionary containing database information, including the target collection.
            search_params (Dict[str, Any]): The search parameters to filter the documents.

        Returns:
            Any: The result of the find_all operation, typically a list of matching documents or an empty list if none found.
        """
        self._logger.debug(f"Finding all documents in collection: {db_data['_collection']}")
        return self.db_adapter.find_all(db_data, search_params)
