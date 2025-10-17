from pydantic import Field
from typing import Any
from ..base import DataModel
from ..utils.enum import ResultDataStatus


class OperationResult(DataModel):
    """
    Represents the outcome of an equipment operation, including its status and any associated data.
    """

    success: bool
    """True if the operation completed successfully; otherwise, False."""

    error: str = Field(default="")
    """Description of the error if the operation failed; empty if successful."""

    result_data: Any = Field(default=None)
    """The data produced by the operation, if any."""

    data_file_name: str = Field(default="")
    """Name of the file containing the result data, including its extension. Leave empty if not applicable."""

    data_type: str = Field(default="")
    """Type or format of the result data (e.g., "image", "text", "json"). """

    data_status: ResultDataStatus = ResultDataStatus.UNAVAILABLE
    """Current availability status of the result data. Defaults to UNAVAILABLE."""

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
