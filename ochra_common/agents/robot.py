from pydantic import Field
from uuid import UUID
from ..spaces.location import Location
from .agent import Agent


class Robot(Agent):
    """
    Abstract robot class to represent a generic robot.

    Attributes:
        type (str): The type of the robot.
        location (Location): The current location of the robot.
        station_id (UUID): The station id where the robot is located.
    """

    type: str
    location: Location = Field(default=None)
    station_id: UUID = Field(default=None)

    _endpoint = "robots"  # associated endpoint for all robots
