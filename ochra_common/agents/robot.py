from dataclasses import dataclass
from ..spaces.location import Location
from .agent import Agent


@dataclass
class Robot(Agent):
    type: str
    location: Location
