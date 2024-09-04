from mongoengine import connect, Document
import logging
import json
from bson import ObjectId
import gridfs


class MongoAdapter:
    """mongodb adapter class"""

    def __init__(
        self,
        hostname: str,
        db_name: str,
        logger: logging.Logger = None,
    ):
        """Constructor for MongoAdapter

        Args:
            hostname (str): address of db host
            db_name (str): name of the db
            logger (logging.Logger, optional): logger if you have one.
                Defaults to None.
        """
        self.url = f"mongodb://{hostname}/"
        self._db_name = db_name
        # connect(db=db_name, host=hostname, alias=db_name)
        self._db_client = connect(db=db_name, host=hostname, alias=db_name)
        self.fs = gridfs.GridFS(self._db_client[self._db_name])

    def clear_collection(self, collection: str):
        """clears the given collection inside the db

        Args:
            collection (str): name of collection

        Returns:
            None
        """
        if self.is_database_existing():
            if collection in self._client[self._db_name].list_collection_names():
                self._client[self._db_name][collection].drop()

    def is_collection_populated(self, collection: str):
        """Check if collection exists on the db

        Args:
            collection (str): name of the collection
        Returns:
            True if collection exists. Otherwise False
        """
        if self.is_database_existing():
            return collection in self._db_client[self._db_name].list_collection_names()

    def delete_database(self) -> None:
        """Deletes database from host

        Args:

        Returns:
            None
        """
        if self.is_database_existing():
            self._db_client.drop_database(self._db_name)

    def is_database_existing(self) -> bool:
        """Check if database exists on the host

        Args:

        Returns:
            True if database exists. Otherwise False
        """
        return self._db_name in self._db_client.list_database_names()

    def create(self, db_data, document: Document):
        """Create a new document in the specified collection."""
        collection = db_data["_collection"]
        collection = self._db_client[self._db_name][collection]
        if hasattr(document, "to_json"):
            return collection.insert_one(json.loads(document.to_json())).inserted_id
        else:
            return collection.insert_one(document).inserted_id

    def read(self, db_data, property, file=False):
        """Read documents from the specified collection that match the query."""
        object_id = db_data["id"]
        collection = db_data["_collection"]
        if file:
            return self.fs.get(object_id).read()

        collection = self._db_client[self._db_name][collection]
        query = {"id": object_id}
        result = collection.find_one(query)

        if property and result is not None:
            return result[property]
        else:
            return result

    def update(self, db_data, update: dict):
        """Update documents in the specified collection that match the query."""
        collection = db_data["_collection"]
        object_id = db_data["id"]
        collection = self._db_client[self._db_name][collection]
        update = {"$set": update}
        query = {"id": object_id}

        return collection.update_many(query, update)

    def delete(self, collection: str, query: dict):
        """Delete documents from the specified collection that match the query."""
        collection = self._db_client[self._db_name][collection]
        return collection.delete_many(query)

    def find(self, db_data, search_params):
        """Find documents from the specified collection that match the query."""
        collection = db_data["_collection"]
        collection = self._db_client[self._db_name][collection]
        return collection.find(search_params)
