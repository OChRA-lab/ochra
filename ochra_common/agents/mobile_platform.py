from pydantic import Field
from typing import Dict, Any
from .robot import Robot


class MobilePlatform(Robot):
    """
    Abstract mobile platform robot that can move.

    Attributes:
        conditions (dict): A dictionary of conditions related to the mobile platform.
    """

    conditions: Dict[str, Any] = Field(default_factory=dict)

    def go_to(self, args: Dict[str, Any]) -> bool:
        """
        Move the mobile platform to a specified location using given args.

        Args:
            args (Dict[str, Any]): Argument needed for robot navigation to the target location.

        Returns:
            bool: True if the platform successfully moved to the location
        """
        raise NotImplementedError
