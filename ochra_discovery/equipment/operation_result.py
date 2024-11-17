from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
from typing import Union, Type

class OperationResult(OperationResult, RestProxyMixinReadOnly):
    def __init__(self, id: UUID):
        super().__init__()
        self._mixin_hook(self._endpoint, id)

    def get_data(self, filename:str = None) -> bool:
        pass