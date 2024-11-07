from pydantic import Field
from typing import Any
from uuid import UUID
from ..base import DataModel


class OperationResult(DataModel):
    """
    Abstract result class to keep results formatted and structured.

    Attributes:
        data_entry_id (uuid.UUID): The unique identifier of the data entry
        success (bool): The outcome of the operation. 
        error (str): The error if the operation failed. Defaulted to None 
        data (Any): Data of the result. Can be any data
        data_file_type (str): The file type of the result. Defaulted to None, which just means the data is saved as raw text
    """

    data_entry_id: UUID
    success: bool
    error: str = Field(default=None)
    data: Any
    data_file_type: str = Field(default=None)

    def put_data(self) -> bool:
        """
        Converts the data into bytestring and uploads the results

        Returns:
            bool: True if the data is converted and uploaded
        """
        raise NotImplementedError

    def get_data(self) -> Any:
        """
        Retrieve the processed data from the result.

        Returns:
            Any: The processed data.
        """
        raise NotImplementedError
