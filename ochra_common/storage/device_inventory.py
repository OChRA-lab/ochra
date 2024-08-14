from dataclasses import dataclass
from .inventory import Inventory
from uuid import UUID


@dataclass
class DeviceInventory(Inventory):
    """
    Abstract class for inventory specific to a device.

    Attributes:
        device_id (UUID): The unique identifier of the device to which the inventory belongs.
    """
    device_id: UUID
