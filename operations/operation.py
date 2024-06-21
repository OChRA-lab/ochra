from .operationModels import OperationDocument, OperationDbModel
from connections.db_connection import DbConnection
from connections.lab_connection import LabConnection
from bson import ObjectId
import json


class Operation:
    """Operation base class
    """

    def __init__(self, cls, **kwargs) -> None:

        self._lab_conn = LabConnection()
        self._db_conn: DbConnection = DbConnection()
        doc_id = self._lab_conn.construct_object(
            cls, "operations",
            **kwargs
        )
        fromDb = self._db_conn.read("operations", doc_id)
        fromDb["id"] = doc_id
        fromDb.pop("_id")
        self._doc = OperationDbModel(**fromDb)

    @property
    def object_id(self) -> ObjectId:
        """
        ObjectId: objects id in mongo database
        """
        return self._doc.id

    @property
    def name(self):
        """
            str: name of the operation
        """
        return self._doc.name

    @property
    def start_timestamp(self):
        """
            timestamp: start timestamp of the operation
        """
        self._doc.start_timestamp = self._db_conn.read(
            self._doc.collection_name,
            self._doc.id,
            "start_timestamp")
        return self._doc.start_timestamp

    @property
    def end_timestamp(self):
        """
            timestamp: end timestamp of the operation
        """
        self._doc.end_timestamp = self._db_conn.read(
            self._doc.collection_name,
            self._doc.id,
            "end_timestamp")
        return self._doc.end_timestamp

    @property
    def arguments(self):
        """
            dict: arguments of the operation
        """
        return self._doc.arguments

    @property
    def status(self):
        """
            str: status of the operation
        """

        self._doc.status = self._db_conn.read(self._doc.collection_name,
                                              self._doc.id, "status")
        return self._doc.status

    @status.setter
    def status(self, status):
        self._doc.status = status
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id, {"status": status})

    @property
    def data(self):
        """ Any: data of the operation
        """
        fromDb = self._db_conn.read(
            self._doc.collection_name, self._doc.id, "data")
        self._doc.data = fromDb
        return self._doc.data

    def toJSON(self):
        """converts the operation to a json string

        Returns:
            str:  json string of the operation
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Operation_(Operation):
    """Operation Backend class

    """

    def __init__(self, name=None, id=None) -> None:
        """initializes the Operation_ class,
        if name is provided it creates a new document
        if id is provided it loads the document from the database

        Args:
            name (str, optional): name of operation. Defaults to None.
            id (ObjectId, optional): id to load operation from db.
                                        Defaults to None.

        Raises:
            Exception: raised if no name or id is provided
            Exception: raised if both name and id are provided
        """
        self._db_conn: DbConnection = DbConnection()
        if name is None and id is None:
            raise Exception("Provide Name or Id")
        elif name is not None and id is not None:
            raise Exception("cannot have both name and id")
        elif name is None:
            fromDb = self._db_conn.read("operations", id)
            fromDb["id"] = id
            fromDb.pop("_id")
            self._doc = OperationDbModel(**fromDb)
        else:

            self._doc = OperationDbModel(name)

            self._doc.id = self._db_conn.create(
                self._doc.collection_name, self._doc)

    def add_data(self, data):
        """adds data to the operation data list

        Args:
            data (Any): data to add to the operation data list
        """
        tempData = self.data
        tempData.append(data)

        self._db_conn.update(self._doc.collection_name,
                             self._doc.id, {"data": tempData})

        self._doc.data = self._db_conn.read(
            self._doc.collection_name, self._doc.id, "data")

    @property
    def start_timestamp(self):
        """
            timestamp: start timestamp of the operation
        """
        return self._doc.start_timestamp

    @property
    def end_timestamp(self):
        """
            timestamp: end timestamp of the operation
        """
        return self._doc.end_timestamp

    @start_timestamp.setter
    def start_timestamp(self, timestamp):
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id, {"start_timestamp": timestamp})
        self._doc.start_timestamp = self._db_conn.read(
            self._doc.collection_name, self._doc.id, "start_timestamp")

    @end_timestamp.setter
    def end_timestamp(self, timestamp):
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id, {"end_timestamp": timestamp})
        self._doc.end_timestamp = self._db_conn.read(
            self._doc.collection_name, self._doc.id, "end_timestamp")
