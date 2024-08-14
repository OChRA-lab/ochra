from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from typing import BinaryIO, Any


@dataclass
class OperationResult(DataModel):
    """
    Abstract result class to keep results formatted and structured.

    Attributes:
        type (str): The type of the result.
        data (BinaryIO): The binary data of the result.
    """
    type: str
    data: BinaryIO

    @abstractmethod
    def retrieve_processed_data() -> Any:
        """
        Retrieve the processed data from the result.

        Returns:
            Any: The processed data.
        """
        pass
