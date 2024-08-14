from dataclasses import dataclass
from .inventory import Inventory
from uuid import UUID


@dataclass
class DeviceInventory(Inventory):
    """Abstract for inventory specific to a device"""
    device_id: UUID
