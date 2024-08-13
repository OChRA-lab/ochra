from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.spaces.station import Station
from ochra_common.equipment.device import Device
from uuid import UUID


@dataclass
class WorkStation(Station):
    devices: list[Device]

    @abstractmethod
    def add_device(self, device: Device) -> bool:
        pass

    @abstractmethod
    def get_device(self, device: Device | str | UUID) -> Device:
        pass

    @abstractmethod
    def remove_device(self, device: Device) -> bool:
        pass
