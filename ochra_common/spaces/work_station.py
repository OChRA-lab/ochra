from pydantic import Field
from typing import List, Union, Type
from uuid import UUID
from .station import Station
from ..equipment.device import Device


class WorkStation(Station):
    """
    WorkStation class that represents a station with devices.

    Attributes:
        devices (List[Device]): A list of devices associated with the workstation.
    """
    devices: List[Type[Device]] = Field(default_factory=list)

    def get_device(self, device_identifier: Union[str, UUID]) -> Type[Device]:
        """
        Retrieve a device from the workstation.

        Args:
            device (Device | str | UUID): The device, its name, or its UUID.

        Returns:
            Device: The retrieved device.
        """
        raise NotImplementedError
