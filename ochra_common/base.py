from typing import Any
import uuid
from pydantic import BaseModel, Field


class DataModel(BaseModel):
    """
    DataModel class that serves as a base for all dataclasses that are to be stored in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the data model instance.
        _collection (str): The name of the collection where the data model will be stored.
        _cls (str): The class name of the data model.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    cls: str = Field(default=None)

    def model_post_init(self, __context: Any) -> None:
        # retrieve the class name in addition to its import path
        self.cls = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return super().model_post_init(__context)

    def to_json(self) -> str:
        """Convert the data model instance to a JSON string.

        Returns:
            str: json string representation of the data model instance.
        """

        return self.model_dump_json()

    def to_dict(self) -> dict:
        """
        Convert the data model instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary representation of the data model instance.
        """
        return self.model_dump()
