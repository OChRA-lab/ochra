from bson import ObjectId, json_util
from dataclasses import dataclass, field, fields, asdict
from datetime import datetime
from abc import ABC, abstractmethod
import json


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
class OperationDbModel(ABC):
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
        return json_util.dumps(asdict(self), indent=4)


if __name__ == "__main__":
    print(OperationResultDbModel(type="test", dataSource=ObjectId()).to_json())
    print(OperationDbModel(name="test", start_timestamp=datetime.now(),
                           end_timestamp=datetime.now(),
                           status="test", arguments={}).to_json())
