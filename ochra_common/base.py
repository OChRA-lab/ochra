import uuid
from abc import ABC
from dataclasses import dataclass, asdict

@dataclass
class DataModel(ABC):
    id: uuid = uuid.uuid4()
    _collection: str
    _cls: str

    def to_json(self):
        return asdict(self)