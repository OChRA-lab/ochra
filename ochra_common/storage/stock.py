from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.spaces.station import Station
from ochra_common.storage.inventory import Inventory
from typing import Any

@dataclass
class Stock(DataModel):
    station: Station
    inventories = list[Inventory]

    @abstractmethod
    def get_by_type(self, type: str|type) -> list[Any]:
        pass
    
    @abstractmethod
    def to_inventory() -> Inventory:
        pass