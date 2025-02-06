from pydantic import Field
from uuid import UUID
from typing import List, Type, Union

from ..base import DataModel
from ..equipment.device import Device
from ..equipment.robot import Robot
from .location import Location
from ..utils.enum import ActivityStatus, StationType
from ..storage.inventory import Inventory


class Station(DataModel):
    """
    Abstract station class that contains information all stations will have.

    Attributes:
        name (str): The name of the station.
        location (Location): The location of the station.
        type (StationType): The type of the station.
        status (ActiveStatus): The status of the station (e.g., idle, busy). Defaults to IDLE.
        locked_by (str): The user that has locked the station. Defaults to an empty string.
        inventory (Inventory): The inventory associated with the station.
        devices (List[Device]): A list of devices associated with the workstation.
    """

    name: str
    location: Location
    type: StationType
    status: ActivityStatus = ActivityStatus.IDLE
    locked_by: str = Field(default="")
    inventory: Inventory = Field(default=None)
    devices: List[Type[Device]] = Field(default_factory=list)

    _endpoint = "stations"  # associated endpoint for all stations

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
