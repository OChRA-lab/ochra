from ochra_common.storage.inventory import Inventory
from ochra_common.utils.mixins import RestProxyMixin
from uuid import UUID
from typing import Literal


class Inventory(Inventory, RestProxyMixin):
    def __init__(
        self,
        owner_id: UUID,
        owner_type: Literal["station", "robot", "device"],
        containers_max_capacity: int,
    ):
        super().__init__(
            owner_id=owner_id,
            owner_type=owner_type,
            containers_max_capacity=containers_max_capacity,
            module_path="ochra_discovery.storage.inventory",
        )
        self._mixin_hook(self._endpoint, self.id)
