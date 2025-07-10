from typing import Any, Self
import uuid
from pydantic import BaseModel, Field


class DataModel(BaseModel):
    """
    DataModel class that serves as a base for all dataclasses that are to be stored in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the data model instance.
        collection (str): The name of the collection where the data model will be stored.
        cls (str): The class name of the data model.
        module_path(str): The module path of the data model.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    collection: str = Field(default=None)
    cls: str = Field(default=None)
    module_path: str = Field(default=None)

    def model_post_init(self, __context: Any) -> None:
        # retrieve the class name in addition to its import path
        self.cls = f"{self.__class__.__name__}" if self.cls is None else self.cls
        return super().model_post_init(__context)

    def get_base_model(self) -> Self:
        """
        Get a base model containing the base information of the model instance.

        Returns:
            DataModel: A base model containing the base information of the model instance.
        """
        return DataModel(
            id=self.id,
            collection=self.collection,
            cls=self.cls,
            module_path=self.module_path,
        )

    def _cleanup(self) -> None:
        """ Clean up the data model instance by deleting it from the database."""
        from  .connections.lab_connection import LabConnection
        lab: LabConnection = LabConnection()
        lab.delete_object(self.collection,self.id)