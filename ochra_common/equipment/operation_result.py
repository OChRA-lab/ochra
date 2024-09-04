from typing import Any
from uuid import UUID
from ..base import DataModel


class OperationResult(DataModel):
    """
    Abstract result class to keep results formatted and structured.

    Attributes:
        type (str): The type of the result.
        data (BinaryIO): The binary data of the result.
    """
    type: str
    data_entry_id: UUID

    def retrieve_processed_data(self) -> Any:
        """
        Retrieve the processed data from the result.

        Returns:
            Any: The processed data.
        """
        raise NotImplementedError
