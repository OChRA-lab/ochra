from ochra_common.equipment.operation import Operation
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID


class Operation(Operation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        """Operation object that represents any command given to a device and its associated data

        Args:
            object_id (UUID): Database id of the operation
        """
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)
