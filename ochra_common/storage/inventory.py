from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List
from ..base import DataModel
from .consumable import Consumable
from .container import Container

_COLLECTION = "inventories"


@dataclass(kw_only=True)
class Inventory(DataModel):
    """
    Abstract class for inventory, contains containers and consumables.

    Attributes:
        containers_max_capacity (int): The maximum capacity of containers in the inventory.
        containers (List[Container]): A list of containers in the inventory. Defaults to an empty list.
        consumables (List[Consumable]): A list of consumables in the inventory. Defaults to an empty list.
    """
    containers_max_capacity: int
    containers: List[Container] = field(default_factory=list)
    consumables: List[Consumable] = field(default_factory=list)

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()

    @abstractmethod
    def add_container(self, container: Container) -> None:
        """
        Add a container to the inventory.

        Args:
            container (Container): The container to be added.
        """
        pass

    @abstractmethod
    def remove_container(self, container: Container) -> None:
        """
        Remove a container from the inventory.

        Args:
            container (Container): The container to be removed.
        """
        pass

    @abstractmethod
    def add_consumable(self, consumable: Consumable) -> None:
        """
        Add a consumable to the inventory.

        Args:
            consumable (Consumable): The consumable to be added.
        """
        pass

    @abstractmethod
    def remove_consumable(self, consumable: Consumable) -> None:
        """
        Remove a consumable from the inventory.

        Args:
            consumable (Consumable): The consumable to be removed.
        """
        pass
