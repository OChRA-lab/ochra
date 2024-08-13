from dataclasses import dataclass
from ..base import DataModel
from .operation import Operation
from ..storage.inventory import Inventory
from enum import Enum


@dataclass
class Device(DataModel):
    name: str
    status: Enum
    operation_history: list[Operation]
    inventory: Inventory
