from pydantic import Field
from typing import Any
from ..base import DataModel
from ..utils.enum import ResultDataStatus


class OperationResult(DataModel):
    """
    Abstract result class to keep results formatted and structured.

    Attributes:
        success (bool): The outcome of the operation.
        error (str): The error if the operation failed. Defaulted to ""
        result_data (Any): Data of the result. Can be any data
        data_file_name (str): The original file type of the result includes the filetype (e.g. .txt, .jpg). Leave as "" if the data_type is defined below
        data_type (str): the python data model ()
        data_status (ResultDataStatus): The current status of the data. Defaulted to UNAVAILABLE
    """

    success: bool
    error: str = Field(default="")
    result_data: Any = Field(default=None)
    data_filename: str = Field(default="")
    data_type: str = Field(default="")
    data_status: ResultDataStatus = ResultDataStatus.UNAVAILABLE

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

    def save_data(self, path: str = None) -> bool:
        """
        Gets the data from the server and saves it to path. If path is not provided,
        saves it using the original name at the current directory

        Args:
            path (str): The path to save the data to. If None, saves it to the current directory using original name.

        Returns:
            bool: True if the data is saved.
        """
        raise NotImplementedError
