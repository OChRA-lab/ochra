from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.spaces.location import Location
from ochra_common.spaces.station import Station
from ochra_common.equipment.device import Device

class WorkStation(DataModel,ABC,Station):
    devices: list[Device]

    @abstractmethod
    def add_device(self, device: Device) -> bool:
        pass

    @abstractmethod
    def get_device(self, device: Device) -> Device:
        pass

    @abstractmethod
    def remove_device(self, device: Device) -> bool:
        pass