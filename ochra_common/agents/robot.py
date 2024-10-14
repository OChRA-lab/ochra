from pydantic import Field
from ..spaces.location import Location
from .agent import Agent


class Robot(Agent):
    """
    Abstract robot class to represent a generic robot.

    Attributes:
        type (str): The type of the robot.
        location (Location): The current location of the robot.
    """
    type: str
    location: Location = Field(default=None)

    _endpoint = "robots"  # associated endpoint for all robots
