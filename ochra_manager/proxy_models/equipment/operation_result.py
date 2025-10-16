from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.utils.enum import ResultDataStatus
from typing import Any


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
