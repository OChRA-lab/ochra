from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixin
from uuid import UUID


class OperationResult(OperationResult, RestProxyMixin):
    def __init__(self, success, error, result_data, data_file_name, data_type, data_status):
        super().__init__(
            success=success,
            error=error,
            result_data=result_data,
            data_file_name=data_file_name,
            data_type=data_type,
            data_status=data_status,
        )
        self._mixin_hook(self._endpoint, object_id=None)
