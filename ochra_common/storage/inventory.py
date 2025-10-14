from pydantic import Field
from typing import List, Type
from ..base import DataModel
from .consumable import Consumable
from .container import Container


class Inventory(DataModel):
    """
    Inventory model representing a collection of containers and consumables.

    An inventory is typically associated with a station or device in the framework.

    Attributes:
        owner (DataModel): Reference to the entity that owns the inventory.
        containers_max_capacity (int): Maximum number of containers allowed.
        containers (List[Type[Container]]): List of container instances in the inventory.
        consumables (List[Consumable]): List of consumable items in the inventory.
    """

    owner: DataModel
    containers_max_capacity: int
    containers: List[Type[Container]] = Field(default_factory=list)
    consumables: List[Consumable] = Field(default_factory=list)

    _endpoint = "storage/inventories"  # associated endpoint for all inventories

    def add_container(self, container: Type[Container]) -> None:
        """
        Add a container to the inventory.

        Args:
            container (Type[Container]): The container to be added.
        """
        raise NotImplementedError

    def remove_container(self, container: Type[Container]) -> None:
        """
        Remove a container from the inventory.

        Args:
            container (Type[Container]): The container to be removed.
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
