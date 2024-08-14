import uuid
from abc import ABC
from dataclasses import dataclass, asdict


@dataclass
class DataModel(ABC):
    """
    DataModel class that serves as a base for all dataclasses that are to be stored in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the data model instance.
        _collection (str): The name of the collection where the data model will be stored.
        _cls (str): The class name of the data model.
    """
    id: uuid.UUID = uuid.uuid4()
    _collection: str
    _cls: str

    def to_json(self):
        """
        Convert the data model instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary representation of the data model instance.
        """
        return asdict(self)
