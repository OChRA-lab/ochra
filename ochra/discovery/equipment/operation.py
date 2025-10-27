from ochra.common.equipment.operation import Operation
from ochra.discovery.equipment.operation_result import OperationResult
from ochra.common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID


class Operation(Operation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        """Operation object that represents any command given to a device and its associated data

        Args:
            object_id (UUID): Database id of the operation
        """
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)

    def get_result_object(self) -> OperationResult:
        """Get the result of the operation

        Returns:
            OperationResult: The result of the operation
        """
        return OperationResult(id=UUID(self.result))

    def get_result_data(self, path: str = None) -> bytes:
        """Get the data of the operation result, optionally saving it to a file.

        Returns:
            bytes: The data of the operation result
        Args:
            path (str): The path to save the data to. If None, does not save the data.
        """
        if path is not None:
            self.get_result_object().save_data(path)
        return self._lab_conn.get_data("operation_results", self.result)