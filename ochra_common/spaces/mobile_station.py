from pydantic import Field
from typing import Type
from .station import Station
from ..equipment.mobile_robot import MobileRobot


class MobileStation(Station):
    """
    MobileStation class that represents a mobile robot treated as a mobile station.

    Attributes:
        mobile_robot (Type[MobileRobot]): The mobile robot comprising the station.
    """

    mobile_robot: Type[MobileRobot] = Field(default=None)
