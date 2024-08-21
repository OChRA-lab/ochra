from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from typing import BinaryIO, Any

_COLLECTION = "operation_results"


@dataclass(kw_only=True)
class OperationResult(DataModel):
    """
    Abstract result class to keep results formatted and structured.

    Attributes:
        type (str): The type of the result.
        data (BinaryIO): The binary data of the result.
    """
    type: str
    data: BinaryIO

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()

    @abstractmethod
    def retrieve_processed_data(self) -> Any:
        """
        Retrieve the processed data from the result.

        Returns:
            Any: The processed data.
        """
        pass
