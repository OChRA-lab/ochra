from dataclasses import dataclass, field
from typing import List
from ..base import DataModel
from .operation import Operation
from ..storage.device_inventory import DeviceInventory
from enum import Enum

_COLLECTION = "devices"


@dataclass(kw_only=True)
class Device(DataModel):
    """
    Abstract device class that contains information all devices will have.

    Attributes:
        name (str): The name of the device.
        inventory (DeviceInventory): The inventory associated with the device.
        status (Enum): The current status of the device.
        operation_history (List[Operation]): A list of operations performed by the device.
        station_id (str): ID of the station which the device belongs to.
    """
    name: str
    inventory: DeviceInventory = None
    status: Enum = -1  # TODO: Define DeviceStatus Enum
    operation_history: List[Operation] = field(
        init=False, default_factory=list)
    station_id: str = field(init=False, default="")  # TODO: use uuid.UUID

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()
