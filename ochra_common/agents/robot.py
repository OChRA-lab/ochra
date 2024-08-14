from dataclasses import dataclass
from ..spaces.location import Location
from .agent import Agent


@dataclass
class Robot(Agent):
    """Abstract robot class to represent a generic robot"""
    type: str
    location: Location
