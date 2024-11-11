from pydantic import Field
from typing import Any
from uuid import UUID
from ..base import DataModel


class OperationResult(DataModel):
    """
    Abstract result class to keep results formatted and structured.

    Attributes:
        success (bool): The outcome of the operation. 
        error (str): The error if the operation failed. Defaulted to None 
        data (Any): Data of the result. Can be any data
        data_file_type (str): The file type of the result. Leave as None if the data_type is defined below
        data_type (str): the python data model () 
    """
    success: bool
    error: str = Field(default="")
    data: Any = Field(default=None)
    data_file_type: str = Field(default="")
    data_type: str = Field(default="")

    _endpoint = "operation_results"  # associated endpoint for all operations

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
