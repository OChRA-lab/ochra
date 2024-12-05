from ochra_common.equipment.operation import Operation
from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
from typing import Union, Type


class Operation(Operation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        """Operation object that represents any command given to a device and its associated data

        Args:
            object_id (UUID): Database id of the operation
        """
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)

    def get_result(self) -> Type[OperationResult]:
        """returns an operation result object which contains the data of the operation

        Returns:
            Type[OperationResult]: Operation Result object
        """
        return self._lab_conn.construct_object("operation_results", self.result)
