from pydantic import Field
from ..base import DataModel
from uuid import UUID
from .inventory import Inventory
from typing import Any, List, Union


class Stock(DataModel):
    """
    Abstract class for stock, which is a collection of inventories and belongs to a particular station.

    Attributes:
        station_id (UUID): The unique identifier of the station to which the stock belongs.
        inventories (List[Inventory]): A list of inventories contained in the stock. Defaults to an empty list. 
    """
    station_id: UUID
    inventories: List[Inventory] = Field(default_factory=list)

    _endpoint = "storage"  # associated endpoint for all stocks

    def get_from_inventory_by_type(self, type: Union[str, type]) -> List[Any]:
        """
        Retrieve items from the inventory by their type.

        Args:
            type (str | type): The type of items to retrieve.

        Returns:
            List[Any]: A List of items matching the specified type.
        """
        raise NotImplementedError

    def to_inventory(self) -> Inventory:
        """
        Convert the stock to a single inventory.

        Returns:
            Inventory: The inventory representation of the stock.
        """
        raise NotImplementedError
