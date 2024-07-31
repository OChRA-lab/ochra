from bson import ObjectId, json_util
from dataclasses import dataclass, field, fields, asdict
from datetime import datetime
from abc import ABC, abstractmethod
import json

OPERATIONDBDEFAULTS = {
    "_cls": "OperationDbModel",
    "id": None,
    "collection_name": "operations",
    "db_name": "ochra_test_db"
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


@dataclass(kw_only=True)
class Operation():
    name: str
    start_timestamp: datetime = None
    end_timestamp: datetime = None
    status: str = None
    data: list[OperationResultDbModel] = field(default_factory=list)
    db_data = OPERATIONDBDEFAULTS

    def to_json(self):
        dict = self.__dict__
        dbEntry = asdict(self)
        for key in dict:
            if not str(key).startswith("_") and key not in dbEntry.keys():
                dbEntry[key] = dict[key]
        return json_util.dumps(asdict(self), indent=4)

    def get_args(self):
        dict = self.__dict__
        dbEntry = asdict(self)
        args = {}
        for key in dict:
            if not str(key).startswith("_") and key not in dbEntry.keys():
                args[key] = dict[key]
        return args


if __name__ == "__main__":
    OperationModel
    print(OperationResultDbModel(type="test", dataSource=ObjectId()).to_json())
    print(OperationDbModel(name="test", start_timestamp=datetime.now(),
                           end_timestamp=datetime.now(),
                           status="test", arguments={}).to_json())
