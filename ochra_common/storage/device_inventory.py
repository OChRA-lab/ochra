from dataclasses import dataclass
from .inventory import Inventory
from uuid import UUID


@dataclass
class DeviceInventory(Inventory):
    device_id: UUID
