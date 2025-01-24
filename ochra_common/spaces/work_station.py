from pydantic import Field
from typing import List, Union, Type
from uuid import UUID
from .station import Station
from ..equipment.device import Device
from ..equipment.robot import Robot


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
            device_identifier (str | UUID): The device name or its UUID.

        Returns:
            Device: The retrieved device.
        """
        raise NotImplementedError

    def get_robot(self, robot_identifier: Union[str, UUID]) -> Type[Robot]:
        """
        Retrieve a robot from the workstation.

        Args:
            robot_identifier (str | UUID): The robot name or its UUID.

        Returns:
            Robot: The retrieved robot.
        """
        raise NotImplementedError
