from pydantic import Field
from uuid import UUID
from typing import List, Type, Union

from ..base import DataModel
from ..equipment.device import Device
from ..equipment.operation import Operation
from ..equipment.robot import Robot
from .location import Location
from ..utils.enum import ActivityStatus, StationType
from ..storage.inventory import Inventory
from uuid import UUID
from typing import Optional

class Station(DataModel):
    """
    Abstract station class that contains information all stations will have.

    Attributes:
        name (str): The name of the station.
        location (Location): The location of the station.
        type (StationType): The type of the station.
        status (ActiveStatus): The status of the station (e.g., idle, busy). Defaults to IDLE.
        inventory (Inventory): The inventory associated with the station.
        devices (List[Device]): A list of devices associated with the workstation.
        operation_record (List[Operation]): Record of the operations assigned to the station.
        locked (UUID): The session ID of the user that has locked the station.
    """

    name: str
    location: Location
    type: StationType
    status: ActivityStatus = ActivityStatus.IDLE
    inventory: Inventory = Field(default=None)
    devices: List[Type[Device]] = Field(default_factory=list)
    operation_record: List[Operation] = Field(default_factory=list)
    locked: Optional[UUID] = Field(defualt=None)

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


    def lock(self, session_id: UUID):
        """Lock the device for the given session."""
        if self.locked == []:
            self.locked = session_id
        elif self.locked != session_id:
            raise Exception(
                f"Device {self.name} is already locked by session {self.locked}."
            )
            

    def unlock(self, session_id: UUID):
        """Unlock the device for the given session."""
        if session_id == "ADMIN":
            self.locked = None
        if self.locked != session_id:
            raise Exception(
                f"Session {session_id} does not have lock on device {self.name}."
            )
        else:
            self.locked = None
