from ochra_common.storage.inventory import Inventory
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.storage.container import Container
from ochra_common.storage.consumable import Consumable
from uuid import UUID
from typing import Type, Literal

class Inventory(Inventory, RestProxyMixin):
    def __init__(self, owner_id: UUID, owner_type: Literal["station", "robot", "device"], containers_max_capacity: int):
        super().__init__(owner_id=owner_id, owner_type=owner_type,
                         containers_max_capacity=containers_max_capacity,
                         module_path="ochra_discovery.storage.inventory")
        self._mixin_hook(self._endpoint, self.id)

    def add_container(self, container: Type[Container]) -> None:
        containers = self.containers
        containers.append(container)
        self.containers = containers

    def remove_container(self, container: Type[Container]) -> None:
        containers = self.containers
        containers.remove(container)
        self.containers = containers

    def add_consumable(self, consumable: Consumable) -> None:
        consumables = self.consumables
        consumables.append(consumable)
        self.consumables = consumables

    def remove_consumable(self, consumable: Consumable) -> None:
        consumables = self.consumables
        consumables.remove(consumable)
        self.consumables = consumables