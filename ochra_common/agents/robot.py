from dataclasses import dataclass
from ..spaces.location import Location
from .agent import Agent


@dataclass
class Robot(Agent):
    """
    Abstract robot class to represent a generic robot.

    Attributes:
        type (str): The type of the robot.
        location (Location): The current location of the robot.
    """
    type: str
    location: Location
