from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from uuid import UUID
from .inventory import Inventory
from typing import Any


@dataclass
class Stock(DataModel):
    """
    Abstract class for stock, which is a collection of inventories and belongs to a particular station.

    Attributes:
        station_id (UUID): The unique identifier of the station to which the stock belongs.
        inventories (list[Inventory]): A list of inventories contained in the stock.
    """
    station_id: UUID
    inventories: list[Inventory]

    @abstractmethod
    def get_from_inventory_by_type(self, type: str | type) -> list[Any]:
        """
        Retrieve items from the inventory by their type.

        Args:
            type (str | type): The type of items to retrieve.

        Returns:
            list[Any]: A list of items matching the specified type.
        """
        pass

    @abstractmethod
    def to_inventory(self) -> Inventory:
        """
        Convert the stock to a single inventory.

        Returns:
            Inventory: The inventory representation of the stock.
        """
        pass
