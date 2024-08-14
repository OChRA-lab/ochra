from abc import abstractmethod
from dataclasses import dataclass
from .station import Station
from ..equipment.device import Device
from uuid import UUID


@dataclass
class WorkStation(Station):
    """
    WorkStation class that represents a station with devices.

    Attributes:
        devices (list[Device]): A list of devices associated with the workstation.
    """
    devices: list[Device]

    @abstractmethod
    def add_device(self, device: Device) -> bool:
        """
        Add a device to the workstation.

        Args:
            device (Device): The device to be added.

        Returns:
            bool: True if the device was added successfully
        """
        pass

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

    @abstractmethod
    def remove_device(self, device: Device) -> bool:
        """
        Remove a device from the workstation.

        Args:
            device (Device): The device to be removed.

        Returns:
            bool: True if the device was removed successfully
        """
        pass
