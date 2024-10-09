from .operation import Operation
from ..utils.mixins import RestProxyMixin

class OperationProxy(Operation,RestProxyMixin):
    def __init__(self, caller_id, method, args):
        super().__init__(caller_id=caller_id, method=method, args=args)
        self._mixin_hook("operations",self.id)