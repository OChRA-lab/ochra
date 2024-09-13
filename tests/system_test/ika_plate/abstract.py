from ochra_common.storage.device_inventory import DeviceInventory
from ochra_common.equipment.device import Device
from ochra_common.equipment.temperature_control import TemperatureControls
from ochra_common.equipment.stir_control import StirControls
from abc import ABC


class IkaPlateInventory(DeviceInventory):
    pass


class IkaPlateAbstract(Device, TemperatureControls, StirControls, ABC):
    temperature: float = 0
    stir_speed: float = 0
    # inventory: DeviceInventory = DeviceInventory([], [], 1,)
