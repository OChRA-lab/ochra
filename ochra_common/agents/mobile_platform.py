from abc import abstractmethod
from dataclasses import dataclass
from .robot import Robot
from ..spaces.location import Location


@dataclass
class MobilePlatform(Robot):
    """
    Abstract mobile platform robot that can move.

    Attributes:
        conditions (dict): A dictionary of conditions related to the mobile platform.
    """
    conditions: dict

    @abstractmethod
    def go_to(self, location: Location) -> bool:
        """
        Move the mobile platform to a specified location.

        Args:
            location (Location): The target location to move to.

        Returns:
            bool: True if the platform successfully moved to the location
        """
        pass
