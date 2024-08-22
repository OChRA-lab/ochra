import uuid
from datetime import datetime, date
from dataclasses import dataclass, asdict, field
import json
from .utils.json_helpers import CustomJSONEncoder


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


@dataclass(kw_only=True)
class DataModel:
    """
    DataModel class that serves as a base for all dataclasses that are to be stored in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the data model instance.
        _collection (str): The name of the collection where the data model will be stored.
        _cls (str): The class name of the data model.
    """
    id: uuid.UUID = field(init=False, default_factory=uuid.uuid4)
    _collection: str = field(init=False, default="")
    _cls: str = field(init=False)

    def __post_init__(self):
        self._cls = self.__class__.__name__

    def to_json(self) -> str:
        """Convert the data model instance to a JSON string.

        Returns:
            str: json string representation of the data model instance.
        """

        out_dict = asdict(self)
        return json.dumps(out_dict, cls=CustomJSONEncoder)

    def to_dict(self) -> dict:
        """
        Convert the data model instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary representation of the data model instance.
        """
        out_dict = asdict(self)
        for key, value in out_dict.items():
            if isinstance(value, uuid.UUID):
                out_dict[key] = value.hex
            elif isinstance(value, (datetime, date)):
                out_dict[key] = value.isoformat()
            elif isinstance(value, bytes):
                # TODO: Check if this is the correct way to handle bytes with json
                out_dict[key] = value.hex()
            elif not is_jsonable({key: value}):
                out_dict[key] = value.to_json()
        return out_dict
