from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.equipment.operation import Operation
from ochra_common.storage.inventory import Inventory
from enum import Enum


@dataclass
class Device(DataModel):
    name: str
    status: Enum
    operation_history: list[Operation]
    inventory: Inventory

    @abstractmethod
    def setup(self, **kwargs) -> None:
        pass
