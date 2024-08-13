from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from uuid import UUID
from ochra_common.storage.inventory import Inventory
from typing import Any


@dataclass
class Stock(DataModel):
    station_id: UUID
    inventories = list[Inventory]

    @abstractmethod
    def get_from_inventory_by_type(self, type: str | type) -> list[Any]:
        pass

    @abstractmethod
    def to_inventory() -> Inventory:
        pass
