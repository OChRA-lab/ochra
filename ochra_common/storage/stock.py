from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from uuid import UUID
from .inventory import Inventory
from typing import Any


@dataclass
class Stock(DataModel):
    """Abstract class for stock, which is a collection of inventories and belongs to a particular station"""
    station_id: UUID
    inventories = list[Inventory]

    @abstractmethod
    def get_from_inventory_by_type(self, type: str | type) -> list[Any]:
        pass

    @abstractmethod
    def to_inventory() -> Inventory:
        pass
