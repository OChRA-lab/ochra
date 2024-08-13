from dataclasses import dataclass
from ochra_common.storage.inventory import Inventory
from uuid import UUID


@dataclass
class DeviceInventory(Inventory):
    device_id: UUID
