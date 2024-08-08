from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.storage.inventory import Inventory
from ochra_common.equipment.device import Device

@dataclass
class DeviceInventory(DataModel, ABC, Inventory):
    device: Device