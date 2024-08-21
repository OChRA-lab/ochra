from abc import abstractmethod
from dataclasses import dataclass, field
from ochra_common.base import DataModel
from uuid import UUID
from .inventory import Inventory
from typing import Any, List

_COLLECTION = "stocks"


@dataclass(kw_only=True)
class Stock(DataModel):
    """
    Abstract class for stock, which is a collection of inventories and belongs to a particular station.

    Attributes:
        station_id (UUID): The unique identifier of the station to which the stock belongs.
        inventories (List[Inventory]): A list of inventories contained in the stock. Defaults to an empty list. 
    """
    station_id: UUID
    inventories: List[Inventory] = field(default_factory=list)

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()

    @abstractmethod
    def get_from_inventory_by_type(self, type: str | type) -> List[Any]:
        """
        Retrieve items from the inventory by their type.

        Args:
            type (str | type): The type of items to retrieve.

        Returns:
            List[Any]: A List of items matching the specified type.
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
