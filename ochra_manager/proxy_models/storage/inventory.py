from ochra_common.storage.inventory import Inventory
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.base import DataModel


class Inventory(Inventory, RestProxyMixin):
    def __init__(
        self,
        owner: DataModel,
        containers_max_capacity: int,
    ):
        super().__init__(
            collection="inventories",
            owner=owner,
            containers_max_capacity=containers_max_capacity,
            module_path="ochra_discovery.storage.inventory",
        )
        self._mixin_hook(self._endpoint, self.id)
