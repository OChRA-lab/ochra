from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixin
from typing import Any
from ochra_common.utils.enum import ResultDataStatus


class OperationResult(OperationResult, RestProxyMixin):
    def __init__(
        self,
        success: bool,
        error: str,
        result_data: Any,
        data_file_name: str,
        data_type: str,
        data_status: ResultDataStatus,
    ):
        """result class to keep results formatted and structured.

        Args:
            success (bool): The outcome of the operation.
            error (str): The error if the operation failed. Defaulted to ""
            result_data (Any): Data of the result. Can be any data
            data_file_name (str): The original file type of the result includes the filetype (e.g. .txt, .jpg). Leave as "" if the data_type is defined below
            data_type (str): the python data model ()
            data_status (enum): The current status of the data. -1 (upload not started), 0 (uploading), 1(upload complete)
        """
        super().__init__(
            collection="operation_results",
            success=success,
            error=error,
            result_data=result_data,
            data_file_name=data_file_name,
            data_type=data_type,
            data_status=data_status,
        )
        self._mixin_hook(self._endpoint, object_id=None)
