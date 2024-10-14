from pydantic import Field
from enum import Enum
from typing import List
from uuid import UUID
from ..base import DataModel
from .operation import Operation
from ..storage.device_inventory import DeviceInventory


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
    inventory: DeviceInventory = Field(default=None)
    status: Enum = -1  # TODO: Define DeviceStatus Enum
    operation_history: List[Operation] = Field(default_factory=list)
    station_id: UUID = Field(default=None)

    _endpoint = "devices" # associated endpoint for all devices