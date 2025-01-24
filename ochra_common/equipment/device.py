from pydantic import Field
from typing import List
from uuid import UUID
from ..base import DataModel
from .operation import Operation
from ..utils.enum import ActiveStatus
from ..storage.inventory import Inventory


class Device(DataModel):
    """
    Abstract device class that contains information all devices will have.

    Attributes:
        name (str): The name of the device.
        inventory (DeviceInventory): The inventory associated with the device.
        status (ActiveStatus): The current active status of the device. Defaults to IDLE.
        operation_history (List[Operation]): A list of operations performed by the device.
        owner_station (str): ID of the station which the device belongs to.
    """

    name: str
    inventory: Inventory = Field(default=None)
    status: ActiveStatus = ActiveStatus.IDLE
    operation_history: List[Operation] = Field(default_factory=list)
    owner_station: UUID = Field(default=None)

    _endpoint = "devices"  # associated endpoint for all devices
