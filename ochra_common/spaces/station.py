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
from typing import Optional

class Station(DataModel):
    """
    Represents a laboratory station containing devices, robots, and inventory.

    Attributes:
        name (str): Station name.
        location (Location): Physical location of the station.
        type (StationType): Station category/type.
        status (ActivityStatus): Current operational status (default: IDLE).
        inventory (Inventory): Inventory associated with the station.
        devices (List[Device]): Devices associated with the station.
        operation_record (List[Operation]): History of operations performed.
        locked (Optional[UUID]): Session ID of the user who has locked the station, if any.
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

    def get_device(self, device_identifier: str| UUID) -> Type[Device]:
        """
        Retrieve a device from the station.

        Args:
            device_identifier (str | UUID): The device name or its unique identifier.

        Returns:
            Type[Device]: The retrieved device.
        """
        raise NotImplementedError

    def get_robot(self, robot_identifier: str| UUID) -> Type[Robot]:
        """
        Retrieve a robot from the station.

        Args:
            robot_identifier (str | UUID): The robot name or its unique identifier.

        Returns:
            Type[Robot]: The retrieved robot.
        """
        raise NotImplementedError


    def lock(self, session_id: UUID):
        """
        Lock the station for the given session.

        Args:
            session_id (UUID): The session ID requesting the lock.

        Raises:
            Exception: If the station is already locked by another session.
        """
        if self.locked == []:
            self.locked = session_id
        elif self.locked != session_id:
            raise Exception(
                f"Device {self.name} is already locked by session {self.locked}."
            )
            

    def unlock(self, session_id: UUID):
        """
        Unlock the station for the given session.

        Args:
            session_id (UUID): The session ID requesting the unlock.

        Raises:
            Exception: If the session does not hold the lock and is not ADMIN.
        """
        if session_id == "ADMIN":
            self.locked = None
        if self.locked != session_id:
            raise Exception(
                f"Session {session_id} does not have lock on device {self.name}."
            )
        else:
            self.locked = None
