from mongoengine import Document, fields
from bson import ObjectId, json_util
from dataclasses import dataclass, field
from datetime import datetime
import json


class OperationResultDocument(Document):
    type = fields.StringField()
    dataSource = fields.ObjectIdField()
    data = fields.FileField("ochra_test_db")

    meta = {
        "collection": "operations_results",
        "db_alias": "ochra_test_db",
        "allow_inheritance": False,
    }


@dataclass
class OperationResultDbModel():
    type: str
    data: ObjectId = None
    collection_name: str = "operations_results"
    db_name: str = "ochra_test_db"
    id: ObjectId = None
    _cls: str = "OperationResultDbModel"

    def to_json(self):
        return json_util.dumps(self.__dict__,
                               default=lambda x: x.__dict__, indent=4)


@dataclass
class OperationDbModel():
    name: str
    _cls: str = "OperationDbModel"
    id: ObjectId = None
    start_timestamp: datetime = None
    end_timestamp: datetime = None
    status: str = None
    arguments: dict = None
    data: list[OperationResultDbModel] = field(default_factory=list)
    collection_name: str = "operations"
    db_name: str = "ochra_test_db"

    def to_json(self):
        return json_util.dumps(self.__dict__,
                               default=lambda x: x.__dict__, indent=4)


class OperationDocument(Document):
    """Operation mongo Document for db model
    """
    name = fields.StringField()
    start_timestamp = fields.DateTimeField()
    end_timestamp = fields.DateTimeField()
    status = fields.StringField(default="idle")
    arguments = fields.DictField()
    data = fields.ListField(fields.ReferenceField(
        OperationResultDocument), default=[])

    meta = {
        "collection": "operations",
        "db_alias": "ochra_test_db",
        "allow_inheritance": False,
    }


if __name__ == "__main__":
    print(OperationResultDbModel(type="test", dataSource=ObjectId()).to_json())
    print(OperationDbModel(name="test", start_timestamp=datetime.now(),
                           end_timestamp=datetime.now(),
                           status="test", arguments={}).to_json())
