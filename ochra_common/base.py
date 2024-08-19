import uuid
from abc import ABC
from dataclasses import dataclass, asdict, field
import json


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


@dataclass(kw_only=True)
class DataModel(ABC):
    """
    DataModel class that serves as a base for all dataclasses that are to be stored in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the data model instance.
        _collection (str): The name of the collection where the data model will be stored.
        _cls (str): The class name of the data model.
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _collection: str
    _cls: str

    def to_json(self):
        """Convert the data model instance to a JSON string.

        Returns:
            str: json string representation of the data model instance.
        """

        selfdict = self.to_dict()
        return json.dumps(selfdict)

    def to_dict(self):
        """
        Convert the data model instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary representation of the data model instance.
        """
        selfdict = asdict(self)
        for key, value in selfdict.items():
            if isinstance(value, uuid.UUID):
                selfdict[key] = value.hex
            elif not is_jsonable({key: value}):
                selfdict[key] = value.to_json()
        return selfdict
