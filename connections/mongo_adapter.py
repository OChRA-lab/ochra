from mongoengine import connect, Document
import logging
import json
from bson import ObjectId
import gridfs


class MongoDbAdapter:
    """mongodb adapter class"""

    def __init__(
        self,
        hostname: str,
        db_name: str,
        logger: logging.Logger = None,
    ):
        """Constructor for MongoDbAdapter

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

    def create(self, collection: str, document: Document):
        """Create a new document in the specified collection."""
        collection = self._db_client[self._db_name][collection]
        return collection.insert_one(json.loads(document.to_json())).inserted_id

    def read(self, collection: str, object_id, property, file=False):
        """Read documents from the specified collection that match the query."""
        if file:
            return self.fs.get(object_id).read()

        collection = self._db_client[self._db_name][collection]
        if type(object_id) is str:
            object_id = ObjectId(object_id)
        query = {"_id": object_id}
        result = collection.find_one(query)

        if property:
            # if result[property].
            return result[property]
        else:
            return result

    def update(self, collection: str, object_id, update: dict):
        """Update documents in the specified collection that match the query."""
        collection = self._db_client[self._db_name][collection]
        update = {"$set": update}
        query = {"_id": object_id}

        return collection.update_many(query, update)

    def delete(self, collection: str, query: dict):
        """Delete documents from the specified collection that match the query."""
        collection = self._db_client[self._db_name][collection]
        return collection.delete_many(query)
