from pydantic import Field
from typing import Dict, Any
from .robot import Robot
from ..spaces.location import Location


class MobilePlatform(Robot):
    """
    Abstract mobile platform robot that can move.

    Attributes:
        conditions (dict): A dictionary of conditions related to the mobile platform.
    """
    conditions: Dict[str, Any] = Field(default_factory=dict)

    def go_to(self, location: Location) -> bool:
        """
        Move the mobile platform to a specified location.

        Args:
            location (Location): The target location to move to.

        Returns:
            bool: True if the platform successfully moved to the location
        """
        raise NotImplementedError
