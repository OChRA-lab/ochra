from typing import Dict, Any
from .robot import Robot
from ..utils.enum import MobileRobotState


class MobileRobot(Robot):
    """
    Abstract class to represent a mobile robot that can move.

    Attributes:
        state (MobileRobotState): State of the mobile robot. Defaults to AVAILABLE
    """

    state: MobileRobotState = MobileRobotState.AVAILABLE

    def go_to(self, args: Dict[str, Any]) -> bool:
        """
        Move the mobile platform to a specified location using given args.

        Args:
            args (Dict[str, Any]): Argument needed for robot navigation to the target location.

        Returns:
            bool: True if the platform successfully moved to the location
        """
        raise NotImplementedError
