from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from .consumable import Consumable
from .container import Container


@dataclass
class Inventory(DataModel):
    """
    Abstract class for inventory, contains containers and consumables.

    Attributes:
        containers (list[Container]): A list of containers in the inventory.
        consumables (list[Consumable]): A list of consumables in the inventory.
        containers_max_capacity (int): The maximum capacity of containers in the inventory.
    """
    containers: list[Container]
    consumables: list[Consumable]
    containers_max_capacity: int

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
