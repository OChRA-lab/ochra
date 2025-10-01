from mongoengine import connect, Document
import logging
import json
import gridfs
from ochra_common.utils.enum import PatchType


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
        collection = self._db_client[self._db_name][collection]
        query = {"id": object_id}
        result = collection.find_one(query)

        if property and result is not None:
            value = result[property]
            if file:
                return self.fs.get(value).read()
            else:
                return value
        else:
            return result

    def update(self, db_data, update: dict, file=False):
        """Update documents in the specified collection that match the query."""
        collection = db_data["_collection"]
        object_id = db_data["id"]
        collection = self._db_client[self._db_name][collection]
        if file:
            file_id = self.fs.put(update["result_data"], encoding="UTF8")
            key = list(update.keys())[0]
            update = {"$set": {key: file_id}}
        else:
            property_name = update["property"]
            property_value = update["property_value"]
            update_type = update["patch_type"]
            update_args = update["patch_args"]
            if update_type == PatchType.SET:
                update = {"$set": {property_name: property_value}}
            elif update_type == PatchType.LIST_APPEND:
                update = {"$push": {property_name: property_value}}
            elif update_type == PatchType.LIST_POP:
                pop_left = -1 if update_args["pop_left"] else 1
                update = {"$pop": {property_name: pop_left}}
            elif update_type == PatchType.LIST_DELETE:
                update = {"$pull": {property_name: property_value}}
            elif update_type == PatchType.LIST_INSERT:
                insert_index = update_args["insert_index"]
                update = {
                    "$push": {
                        property_name: {"$each": property_value},
                        "$position": insert_index,
                    }
                }
            elif update_type == PatchType.DICT_INSERT:
                key = update_args["key"]
                update = {"$set": {f"{property_name}.{key}": property_value}}
            elif update_type == PatchType.DICT_DELETE:
                key = update_args["key"]
                update = {"$unset": {f"{property_name}.{key}": ""}}

        query = {"id": object_id}

        return collection.update_many(query, update)

    def delete(self, db_data):
        """Delete documents from the specified collection that match the query."""
        collection = self._db_client[self._db_name][db_data["_collection"]]
        query = {"id": db_data["id"]}
        return collection.delete_many(query)

    def find(self, db_data, search_params):
        """Find a document from the specified collection that match the query."""
        collection = db_data["_collection"]
        collection = self._db_client[self._db_name][collection]
        result = collection.find_one(search_params)
        if result is not None:
            result.pop("_id")
        return result

    def find_all(self, db_data, search_params):
        """Find all documents from the specified collection that match the query."""
        collection = db_data["_collection"]
        collection = self._db_client[self._db_name][collection]
        results = collection.find(search_params)
        results_list = []
        for result in results:
            result.pop("_id")
            results_list.append(result)
        return results_list
