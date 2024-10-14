from pydantic import Field
from typing import List, Type
from ..base import DataModel
from .consumable import Consumable
from .container import Container


class Inventory(DataModel):
    """
    Abstract class for inventory, contains containers and consumables.

    Attributes:
        containers_max_capacity (int): The maximum capacity of containers in the inventory.
        containers (List[Container]): A list of containers in the inventory. Defaults to an empty list.
        consumables (List[Consumable]): A list of consumables in the inventory. Defaults to an empty list.
    """
    containers_max_capacity: int
    containers: List[Type[Container]] = Field(default_factory=list)
    consumables: List[Consumable] = Field(default_factory=list)

    _endpoint = "storage"  # associated endpoint for all inventories

    def add_container(self, container: Type[Container]) -> None:
        """
        Add a container to the inventory.

        Args:
            container (Container): The container to be added.
        """
        raise NotImplementedError

    def remove_container(self, container: Type[Container]) -> None:
        """
        Remove a container from the inventory.

        Args:
            container (Container): The container to be removed.
        """
        raise NotImplementedError

    def add_consumable(self, consumable: Consumable) -> None:
        """
        Add a consumable to the inventory.

        Args:
            consumable (Consumable): The consumable to be added.
        """
        raise NotImplementedError

    def remove_consumable(self, consumable: Consumable) -> None:
        """
        Remove a consumable from the inventory.

        Args:
            consumable (Consumable): The consumable to be removed.
        """
        raise NotImplementedError
