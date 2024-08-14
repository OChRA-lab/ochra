from dataclasses import dataclass
from ..base import DataModel
from .operation import Operation
from ..storage.inventory import Inventory
from enum import Enum


@dataclass
class Device(DataModel):
    """
    Abstract device class that contains information all devices will have.

    Attributes:
        name (str): The name of the device.
        status (Enum): The current status of the device.
        operation_history (list[Operation]): A list of operations performed by the device.
        inventory (Inventory): The inventory associated with the device.
    """
    name: str
    status: Enum
    operation_history: list[Operation]
    inventory: Inventory
