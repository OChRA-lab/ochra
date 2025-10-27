from ochra.common.base.data_model import DataModel
from ochra.common.storage.inventory import Inventory
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.storage.container import Container
from ochra.common.storage.consumable import Consumable
from ochra.common.utils.enum import PatchType
from typing import Type


class Inventory(Inventory, RestProxyMixin):
    """
    Abstract class for inventory, contains containers and consumables.

    Attributes:
        owner (DataModel): The owner of the inventory.
        containers_max_capacity (int): The maximum capacity of containers in the inventory.
        containers (List[Container]): A list of containers in the inventory. Defaults to an empty list.
        consumables (List[Consumable]): A list of consumables in the inventory. Defaults to an empty list.
    """
    def __init__(
        self,
        owner: DataModel,
        containers_max_capacity: int,
    ):
        super().__init__(
            owner=owner,
            containers_max_capacity=containers_max_capacity,
            collection="inventories",
            module_path="ochra.discovery.storage.inventory",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_container(self, container: Type[Container]) -> None:
        """
        Add a container to the inventory.

        Args:
            container (Container): The container to be added.
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "containers", container, PatchType.LIST_APPEND)

    def remove_container(self, container: Type[Container]) -> None:
        """
        Remove a container from the inventory.

        Args:
            container (Container): The container to be removed.
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "containers", container, PatchType.LIST_DELETE)

    def add_consumable(self, consumable: Consumable) -> None:
        """
        Add a consumable to the inventory.

        Args:
            consumable (Consumable): The consumable to be added.
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "consumables", consumable, PatchType.LIST_APPEND)

    def remove_consumable(self, consumable: Consumable) -> None:
        """
        Remove a consumable from the inventory.

        Args:
            consumable (Consumable): The consumable to be removed.
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "consumables", consumable, PatchType.LIST_DELETE)
