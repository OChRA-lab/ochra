from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List
from .station import Station
from ..equipment.device import Device
from uuid import UUID


@dataclass
class WorkStation(Station):
    """
    WorkStation class that represents a station with devices.

    Attributes:
        devices (List[Device]): A list of devices associated with the workstation.
    """
    devices: List[Device] = field(default_factory=list)

    @abstractmethod
    def get_device(self, device: Device | str | UUID) -> Device:
        """
        Retrieve a device from the workstation.

        Args:
            device (Device | str | UUID): The device, its name, or its UUID.

        Returns:
            Device: The retrieved device.
        """
        pass
